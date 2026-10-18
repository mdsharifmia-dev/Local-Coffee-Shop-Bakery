/* =========================================================
   LOCAL COFFEE SHOP & BAKERY - JAVASCRIPT
   ========================================================= */

/* 
 * CONFIGURATION: 
 * Set your coffee shop's WhatsApp phone number with country code (e.g. "88017XXXXXXXX" or "15551234567")
 * If left empty, it will open WhatsApp with the pre-filled order for the customer to pick a recipient.
 */
const COFFEE_SHOP_WHATSAPP_NUMBER = ""; 

document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       1. MOBILE HAMBURGER MENU
       ========================================================= */
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.getElementById("navLinks");

    if (hamburger && navLinks) {
        hamburger.addEventListener("click", function () {
            navLinks.classList.toggle("show");
        });

        // Close menu after clicking any nav link
        const navigationLinks = navLinks.querySelectorAll("a");
        navigationLinks.forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("show");
            });
        });
    }

    /* =========================================================
       2. MENU CATEGORY FILTERING (All, Drinks, Pastries)
       ========================================================= */
    const filterButtons = document.querySelectorAll(".filter-btn");
    const drinksGroup = document.getElementById("drinksGroup");
    const pastriesGroup = document.getElementById("pastriesGroup");

    if (filterButtons.length > 0) {
        filterButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                // Update active button state
                filterButtons.forEach(btn => btn.classList.remove("active"));
                this.classList.add("active");

                const filter = this.getAttribute("data-filter");

                if (drinksGroup && pastriesGroup) {
                    if (filter === "all") {
                        drinksGroup.style.display = "block";
                        pastriesGroup.style.display = "block";
                    } else if (filter === "drinks") {
                        drinksGroup.style.display = "block";
                        pastriesGroup.style.display = "none";
                    } else if (filter === "pastries") {
                        drinksGroup.style.display = "none";
                        pastriesGroup.style.display = "block";
                    }
                }
            });
        });
    }

    /* =========================================================
       3. CONTACT FORM
       ========================================================= */
    const contactForm = document.getElementById("contactForm");
    if (contactForm) {
        contactForm.addEventListener("submit", function (event) {
            event.preventDefault();
            const name = document.getElementById("name") ? document.getElementById("name").value : "Guest";
            alert(`Thank you, ${name}! Your message has been received. We will get back to you shortly.`);
            contactForm.reset();
        });
    }

    /* Close order modal on clicking outside or ESC key */
    const orderModalBackdrop = document.getElementById("orderModal");
    if (orderModalBackdrop) {
        orderModalBackdrop.addEventListener("click", function (e) {
            if (e.target === orderModalBackdrop) {
                closeOrderModal();
            }
        });

        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape") {
                closeOrderModal();
            }
        });
    }

});


/* =========================================================
   4. ORDER POPUP MODAL & WHATSAPP INTEGRATION
   ========================================================= */

let currentOrder = {
    name: "Espresso",
    unitPrice: 3.50,
    qty: 1
};

function openOrderModal(itemName, itemPrice) {
    currentOrder.name = itemName;
    currentOrder.unitPrice = parseFloat(itemPrice);
    currentOrder.qty = 1;

    const modal = document.getElementById("orderModal");
    const modalItemName = document.getElementById("modalItemName");
    const modalItemPrice = document.getElementById("modalItemPrice");
    const modalQty = document.getElementById("modalQty");
    const notesInput = document.getElementById("orderNotes");

    if (modalItemName) modalItemName.textContent = currentOrder.name;
    if (modalItemPrice) modalItemPrice.textContent = `$${currentOrder.unitPrice.toFixed(2)}`;
    if (modalQty) modalQty.textContent = currentOrder.qty;
    if (notesInput) notesInput.value = "";

    if (modal) {
        modal.classList.add("show");
    }
}

function closeOrderModal() {
    const modal = document.getElementById("orderModal");
    if (modal) {
        modal.classList.remove("show");
    }
}

function changeQty(delta) {
    currentOrder.qty = Math.max(1, currentOrder.qty + delta);
    const modalQty = document.getElementById("modalQty");
    const modalItemPrice = document.getElementById("modalItemPrice");

    if (modalQty) modalQty.textContent = currentOrder.qty;
    if (modalItemPrice) {
        const total = (currentOrder.unitPrice * currentOrder.qty).toFixed(2);
        modalItemPrice.textContent = `$${total}`;
    }
}

function submitWhatsAppOrder() {
    const customerName = document.getElementById("customerName") ? document.getElementById("customerName").value.trim() : "";
    const notes = document.getElementById("orderNotes") ? document.getElementById("orderNotes").value.trim() : "";
    const total = (currentOrder.unitPrice * currentOrder.qty).toFixed(2);

    let message = `Hello! I would like to place an order at Local Coffee Shop:\n\n`;
    message += `☕ Item: ${currentOrder.qty}x ${currentOrder.name}\n`;
    message += `💰 Total: $${total}\n`;
    if (notes) {
        message += `📝 Notes: ${notes}\n`;
    }
    if (customerName) {
        message += `👤 Name: ${customerName}\n`;
    }
    message += `\nPlease confirm my order!`;

    // WhatsApp Click to Chat URL (with phone number if configured)
    const encoded = encodeURIComponent(message);
    const whatsappUrl = (typeof COFFEE_SHOP_WHATSAPP_NUMBER === "string" && COFFEE_SHOP_WHATSAPP_NUMBER.trim() !== "")
        ? `https://wa.me/${COFFEE_SHOP_WHATSAPP_NUMBER.trim()}?text=${encoded}`
        : `https://wa.me/?text=${encoded}`;

    window.open(whatsappUrl, "_blank", "noopener,noreferrer");
    closeOrderModal();
}

function submitDirectOrder() {
    const customerName = document.getElementById("customerName") ? document.getElementById("customerName").value.trim() : "Valued Customer";
    const total = (currentOrder.unitPrice * currentOrder.qty).toFixed(2);

    alert(`Thank you, ${customerName}!\n\nYour order for ${currentOrder.qty}x ${currentOrder.name} ($${total}) has been prepared for Pickup at the counter.`);
    closeOrderModal();
}
