resource "aws_security_group" "efs" {
  name        = "pingpong-efs-sg"
  description = "EFS for pingpong postgres"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description     = "NFS from task"
    from_port       = 2049
    to_port         = 2049
    protocol        = "tcp"
    security_groups = [aws_security_group.pingpong.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_efs_file_system" "pg" {
  creation_token = "pingpong-postgres"
  encrypted      = true

  tags = { Name = "pingpong-postgres" }
}

resource "aws_efs_mount_target" "pg" {
  for_each        = toset(data.aws_subnets.default.ids)
  file_system_id  = aws_efs_file_system.pg.id
  subnet_id       = each.value
  security_groups = [aws_security_group.efs.id]
}
