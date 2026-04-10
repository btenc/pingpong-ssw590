function toggleDropdown(triggerButton) {
  const dropdown = triggerButton.closest(".dropdown");
  const menu = dropdown.querySelector(".dropdown-menu");

  const isExpanded = triggerButton.getAttribute("aria-expanded") === true;

  if (menu.classList.contains("hidden")) {
    menu.classList.remove("hidden");

    if (isExpanded) {
      menu.classList.add("hidden");
      triggerButton.setAttribute("aria-expanded", "false");
    
    } else {
      menu.classList.remove("hidden");
      triggerButton.setAttribute("aria-expanded", "true");
    }

    document.querySelectorAll(".dropdown-menu").forEach(m => {
      if (menu !== m) {
        m.classList.add("hidden");
        
        const siblingTrigger = m.parentElement.querySelector("[aria-haspopup]");
        if (siblingTrigger) siblingTrigger.setAttribute("aria-expanded", "false");
      }
    })
  } else {
    menu.classList.add("hidden");
  }
}

document.addEventListener("click", function(event) {
  if (!event.target.closest(".dropdown")) {
    document.querySelectorAll('[aria-expanded="true"]').forEach(trigger => {
      const m = trigger.closest(".dropdown").querySelector(".dropdown-menu");

      if (m) {
        m.classList.add("hidden");
        trigger.setAttribute("aria-expanded", "false");
      }
    })
  }
})