/* =========================================================
   LOCAL COFFEE SHOP & BAKERY - JAVASCRIPT
   ========================================================= */

/* 
 * CONFIGURATION: 
 * Set your coffee shop's contact & payment details here:
 */
const COFFEE_SHOP_WHATSAPP_NUMBER = ""; // e.g. "88017XXXXXXXX" or "15551234567"
const COFFEE_SHOP_BKASH_NUMBER = "017XXXXXXXX"; // Your bKash Personal or Merchant number
const COFFEE_SHOP_NAGAD_NUMBER = "017XXXXXXXX"; // Your Nagad Personal or Merchant number 

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
    qty: 1,
    paymentMethod: "Cash on Delivery / Counter"
};

function selectPaymentMethod(method) {
    const cards = document.querySelectorAll(".payment-card");
    cards.forEach(card => card.classList.remove("active"));

    const instructionsBox = document.getElementById("paymentInstructionsBox");
    const payNumberText = document.getElementById("payNumberText");
    const payInstrText = document.getElementById("payInstrText");

    if (method === "bkash") {
        currentOrder.paymentMethod = "bKash";
        if (instructionsBox) instructionsBox.style.display = "block";
        if (payInstrText) payInstrText.textContent = "Please Send Money to our bKash number:";
        if (payNumberText) payNumberText.textContent = COFFEE_SHOP_BKASH_NUMBER;
    } else if (method === "nagad") {
        currentOrder.paymentMethod = "Nagad";
        if (instructionsBox) instructionsBox.style.display = "block";
        if (payInstrText) payInstrText.textContent = "Please Send Money to our Nagad number:";
        if (payNumberText) payNumberText.textContent = COFFEE_SHOP_NAGAD_NUMBER;
    } else if (method === "card") {
        currentOrder.paymentMethod = "Card at Pickup";
        if (instructionsBox) instructionsBox.style.display = "none";
    } else {
        currentOrder.paymentMethod = "Cash on Delivery / Counter";
        if (instructionsBox) instructionsBox.style.display = "none";
    }

    // Set active state on the corresponding card
    cards.forEach(card => {
        const input = card.querySelector('input[type="radio"]');
        if (input && input.value.toLowerCase().includes(method)) {
            card.classList.add("active");
            input.checked = true;
        }
    });
}

function openOrderModal(itemName, itemPrice) {
    currentOrder.name = itemName;
    currentOrder.unitPrice = parseFloat(itemPrice);
    currentOrder.qty = 1;
    currentOrder.paymentMethod = "Cash on Delivery / Counter";

    const modal = document.getElementById("orderModal");
    const modalItemName = document.getElementById("modalItemName");
    const modalItemPrice = document.getElementById("modalItemPrice");
    const modalQty = document.getElementById("modalQty");
    const notesInput = document.getElementById("orderNotes");
    const trxInput = document.getElementById("trxIdInput");
    const nameInput = document.getElementById("customerName");

    if (modalItemName) modalItemName.textContent = currentOrder.name;
    if (modalItemPrice) modalItemPrice.textContent = `$${currentOrder.unitPrice.toFixed(2)}`;
    if (modalQty) modalQty.textContent = currentOrder.qty;
    if (notesInput) notesInput.value = "";
    if (trxInput) trxInput.value = "";
    if (nameInput) nameInput.value = "";

    selectPaymentMethod("cash");

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
    const trxId = document.getElementById("trxIdInput") ? document.getElementById("trxIdInput").value.trim() : "";
    const total = (currentOrder.unitPrice * currentOrder.qty).toFixed(2);

    let paymentText = currentOrder.paymentMethod;
    if ((currentOrder.paymentMethod === "bKash" || currentOrder.paymentMethod === "Nagad") && trxId) {
        paymentText += ` (TrxID / Sender: ${trxId})`;
    }

    let message = `Hello! I would like to place an order at Local Coffee Shop:\n\n`;
    message += `☕ Item: ${currentOrder.qty}x ${currentOrder.name}\n`;
    message += `💰 Total: $${total}\n`;
    message += `💳 Payment: ${paymentText}\n`;
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
    const trxId = document.getElementById("trxIdInput") ? document.getElementById("trxIdInput").value.trim() : "";
    const total = (currentOrder.unitPrice * currentOrder.qty).toFixed(2);

    let paymentInfo = currentOrder.paymentMethod;
    if (trxId) paymentInfo += ` (Ref: ${trxId})`;

    alert(`Thank you, ${customerName}!\n\nYour order for ${currentOrder.qty}x ${currentOrder.name} ($${total}) has been received.\n\nPayment Method: ${paymentInfo}\nStatus: Ready for Pickup soon at the counter.`);
    closeOrderModal();
}
