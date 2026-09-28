function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute("content") : "";
}

// Toast notification helper
function showToast(message, type = 'success') {
  let toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.className = 'fixed bottom-6 right-6 z-50 flex flex-col gap-3 pointer-events-none';
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.className = `pointer-events-auto transform transition-all duration-300 translate-y-4 opacity-0 flex items-center gap-3 px-5 py-3.5 rounded-2xl shadow-wellness-lg text-sm font-medium border ${
    type === 'success' 
      ? 'bg-brand-dark text-brand-cream border-brand-light/30' 
      : 'bg-red-900/95 text-white border-red-700/50'
  }`;
  
  const icon = type === 'success'
    ? `<svg class="w-5 h-5 text-brand-accent shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>`
    : `<svg class="w-5 h-5 text-red-300 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>`;

  toast.innerHTML = `${icon}<span>${message}</span>`;
  toastContainer.appendChild(toast);

  // Trigger enter animation
  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-4', 'opacity-0');
    toast.classList.add('translate-y-0', 'opacity-100');
  });

  // Auto-remove after 3.5s
  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function updateItem(id, action) {
  fetch(`/${action}_item/${id}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document
          .querySelectorAll(`.quantity-${id}`)
          .forEach((element) => (element.innerHTML = data.quantity));
        const totalPriceEl = document.querySelector(`.totalPrice`);
        if (totalPriceEl) totalPriceEl.innerHTML = data.total_price;
        
        if (data.quantity == 0) {
          document.querySelectorAll(`.cart-${id}`).forEach((element) => {
            element.style.opacity = '0';
            element.style.transform = 'scale(0.95)';
            setTimeout(() => element.remove(), 250);
          });
          showToast('Item removed from cart');
        }
        
        if (data.quantity > 1) {
          document.querySelectorAll(`.icon-${id}`).forEach(
            (element) =>
              (element.innerHTML = `<svg class="w-4 h-4 text-brand-text-dark/70 hover:text-brand-dark" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M20 12H4"/></svg>`)
          );
        } else if (data.quantity === 1) {
          document.querySelectorAll(`.icon-${id}`).forEach(
            (element) =>
              (element.innerHTML = `<svg class="w-4 h-4 text-red-600/80 hover:text-red-700" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>`)
          );
        }
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      showToast('Could not update cart', 'error');
    });
}

function addToCart(id) {
  fetch(`/add_to_cart/${id}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        showToast(data.message || "Added to cart successfully");
        // Animate cart badge if present
        const badge = document.getElementById('cart-badge');
        if (badge) {
          badge.classList.remove('scale-100');
          badge.classList.add('scale-125');
          setTimeout(() => {
            badge.classList.remove('scale-125');
            badge.classList.add('scale-100');
          }, 300);
        }
      }
    })
    .catch((err) => {
      console.error(err);
      showToast("Error adding product to cart", "error");
    });
}

function toggleMore() {
  const options = document.querySelector('.options');
  if (options) {
    options.classList.toggle('display');
    options.classList.toggle('hidden');
  }
}

function toggleMobileMenu() {
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileMenu) {
    mobileMenu.classList.toggle('hidden');
  }
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
  const profileDropdown = document.querySelector('.profile-dropdown-container');
  const options = document.querySelector('.options');
  if (options && !options.classList.contains('hidden') && !options.classList.contains('display')) {
    if (profileDropdown && !profileDropdown.contains(e.target)) {
      options.classList.add('hidden');
      options.classList.add('display');
    }
  }
});





