resource "aws_security_group" "pingpong" {
  name        = "pingpong-sg"
  description = "pingpong ECS task"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "app"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_cloudwatch_log_group" "pingpong" {
  name              = "/ecs/pingpong"
  retention_in_days = 7
}

resource "aws_iam_role" "ecs_execution" {
  name = "pingpong-ecs-execution"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_cluster" "this" {
  name = "pingpong"
}

resource "aws_ecs_task_definition" "pingpong" {
  family                   = "pingpong"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_execution.arn

  volume {
    name = "postgres-data"
    efs_volume_configuration {
      file_system_id     = aws_efs_file_system.pg.id
      transit_encryption = "ENABLED"
    }
  }

  container_definitions = jsonencode([
    {
      name      = "postgres"
      image     = "postgres:16"
      essential = true
      environment = [
        { name = "POSTGRES_DB",       value = "pingpong" },
        { name = "POSTGRES_USER",     value = "pingpong" },
        { name = "POSTGRES_PASSWORD", value = "pingpong" },
        # EFS mount root often has lost+found; use a subdir for PGDATA
        { name = "PGDATA",            value = "/var/lib/postgresql/data/pgdata" }
      ]
      mountPoints = [
        {
          sourceVolume  = "postgres-data"
          containerPath = "/var/lib/postgresql/data"
          readOnly      = false
        }
      ]
      portMappings = [
        { containerPort = 5432, protocol = "tcp" }
      ]
      healthCheck = {
        command  = ["CMD-SHELL", "pg_isready -U pingpong -d pingpong"]
        interval = 5
        timeout  = 5
        retries  = 5
      }
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.pingpong.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "postgres"
        }
      }
    },
    {
      name      = "pingpong"
      image     = "ghcr.io/btenc/pingpong-ssw590:9ba4cf3"
      essential = true
      environment = [
        { name = "HOST",        value = "0.0.0.0" },
        { name = "DB_NAME",     value = "pingpong" },
        { name = "DB_USER",     value = "pingpong" },
        { name = "DB_PASSWORD", value = "pingpong" },
        { name = "DB_HOST",     value = "localhost" },
        { name = "DB_PORT",     value = "5432" }
      ]
      portMappings = [
        { containerPort = 5000, hostPort = 5000, protocol = "tcp" }
      ]
      dependsOn = [
        { containerName = "postgres", condition = "HEALTHY" }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.pingpong.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "pingpong"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "pingpong" {
  name            = "pingpong"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.pingpong.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.pingpong.id]
    assign_public_ip = true
  }

  # Don't start the service until EFS mount targets exist
  depends_on = [aws_efs_mount_target.pg]
}

output "cluster_name" {
  value = aws_ecs_cluster.this.name
}

output "service_name" {
  value = aws_ecs_service.pingpong.name
}

output "efs_id" {
  value = aws_efs_file_system.pg.id
}
