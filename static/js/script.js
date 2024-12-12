function getCSRFToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
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
        document.querySelector(`.totalPrice`).innerHTML = data.total_price;
        console.log(data.quantity);
        if(data.quantity == 0){
          document.querySelectorAll(`.cart-${id}`).forEach(element => element.remove())
        }
        if (data.quantity > 1) {
          document.querySelectorAll(`.icon-${id}`).forEach(
            (element) =>
              (element.innerHTML = `<svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 -960 960 960"
            >
              <path d="M200-440v-80h560v80H200Z" /></svg>`)
          );
        } else {
          document.querySelectorAll(`.icon-${id}`).forEach(
            (element) =>
              (element.innerHTML = `<svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 -960 960 960"
            >
              <path
              d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"
            /></svg>`)
          );
        }
      }
    })
    .catch((error) => {
      console.error("Error:", error);
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
        alert(data.message);
      }
    });
}

function toggleMore(){
  document.querySelector('.options').classList.toggle('display')
}




