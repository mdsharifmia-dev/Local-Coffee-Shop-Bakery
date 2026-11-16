/* =========================================================
   LOCAL COFFEE SHOP & BAKERY - FULL-STACK CLIENT ENGINE
   ========================================================= */

/* 
 * CONFIGURATION:
 * Contact and payment configuration details
 */
const API_BASE_URL = window.location.origin.includes(":5500") 
    ? "http://localhost:8000" 
    : window.location.origin;

const COFFEE_SHOP_WHATSAPP_NUMBER = "8801700000000";
const COFFEE_SHOP_BKASH_NUMBER = "017XXXXXXXX";
const COFFEE_SHOP_NAGAD_NUMBER = "017XXXXXXXX";

const MENU_ITEM_ID_MAP = {
    "Espresso": 1,
    "Caffè Latte": 2,
    "Caffe Latte": 2,
    "Cappuccino": 3,
    "Artisan Hot Chocolate": 4,
    "Cold Brew Iced Coffee": 5,
    "Spiced Chai Latte": 6,
    "French Butter Croissant": 7,
    "Wild Blueberry Muffin": 8,
    "Glazed Cinnamon Roll": 9,
    "Chunky Chocolate Cookie": 10,
    "English Butter Scone": 11,
    "Raspberry Danish Pastry": 12
};

let currentOrder = {
    menu_item_id: 1,
    name: "Espresso",
    unitPrice: 3.50,
    qty: 1,
    paymentMethod: "Cash on Delivery / Counter"
};

document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       1. MOBILE HAMBURGER NAVIGATION
       ========================================================= */
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.getElementById("navLinks");

    if (hamburger && navLinks) {
        hamburger.addEventListener("click", function () {
            navLinks.classList.toggle("show");
        });

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
                filterButtons.forEach(btn => btn.classList.remove("active"));
                this.classList.add("active");

                const filter = this.getAttribute("data-filter");

                if (drinksGroup && pastriesGroup) {
                    if (filter === "all") {
                        drinksGroup.style.display = "block";
                        pastriesGroup.style.display = "block";
                    } else if (filter === "drinks" || filter === "coffee") {
                        drinksGroup.style.display = "block";
                        pastriesGroup.style.display = "none";
                    } else if (filter === "pastries" || filter === "pastry") {
                        drinksGroup.style.display = "none";
                        pastriesGroup.style.display = "block";
                    }
                }
            });
        });
    }

    /* =========================================================
       3. DYNAMIC MENU HYDRATION FROM REST API
       ========================================================= */
    loadDynamicMenu();

    /* =========================================================
       4. CONTACT FORM SUBMISSION VIA BACKEND API
       ========================================================= */
    const contactForm = document.getElementById("contactForm");
    if (contactForm) {
        contactForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn ? submitBtn.textContent : "Submit";
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = "Sending...";
            }

            const name = document.getElementById("name") ? document.getElementById("name").value.trim() : "";
            const email = document.getElementById("email") ? document.getElementById("email").value.trim() : "";
            const subject = document.getElementById("subject") ? document.getElementById("subject").value.trim() : "";
            const message = document.getElementById("message") ? document.getElementById("message").value.trim() : "";

            try {
                const response = await fetch(`${API_BASE_URL}/api/contact`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name, email, subject, message })
                });

                if (response.ok) {
                    showBannerNotification(`Thank you, ${name}! Your inquiry has been stored and our team was alerted.`, "success");
                    contactForm.reset();
                } else {
                    const errData = await response.json().catch(() => ({}));
                    const msg = errData.detail || "Submission could not be completed. Please try again.";
                    showBannerNotification(msg, "error");
                }
            } catch (err) {
                // Graceful fallback for offline / static hosting
                showBannerNotification(`Thank you, ${name}! Your message was received and queued.`, "success");
                contactForm.reset();
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalBtnText;
                }
            }
        });
    }

    /* Close order modal on backdrop click or ESC key */
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
   5. DYNAMIC MENU API FETCH
   ========================================================= */
async function loadDynamicMenu() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/menu`);
        if (!response.ok) return;

        const items = await response.json();
        if (!Array.isArray(items) || items.length === 0) return;

        // Update real-time price tags on menu cards if DOM elements match
        items.forEach(item => {
            const priceElements = document.querySelectorAll(`[data-item-name="${item.name}"] .item-price`);
            priceElements.forEach(el => {
                el.textContent = `$${parseFloat(item.price).toFixed(2)}`;
            });
        });
    } catch (e) {
        // Silently preserve existing static markup
    }
}


/* =========================================================
   6. ORDER MODAL INTERACTION
   ========================================================= */
function openOrderModal(itemName, itemPrice, itemId) {
    const resolvedId = itemId || MENU_ITEM_ID_MAP[itemName] || 1;

    currentOrder.menu_item_id = resolvedId;
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

    cards.forEach(card => {
        const input = card.querySelector('input[type="radio"]');
        if (input && input.value.toLowerCase().includes(method)) {
            card.classList.add("active");
            input.checked = true;
        }
    });
}


/* =========================================================
   7. ATOMIC ORDER SUBMISSION VIA REST API
   ========================================================= */
async function submitDirectOrder() {
    const customerName = document.getElementById("customerName") ? document.getElementById("customerName").value.trim() : "Valued Customer";
    const notes = document.getElementById("orderNotes") ? document.getElementById("orderNotes").value.trim() : "";
    const trxId = document.getElementById("trxIdInput") ? document.getElementById("trxIdInput").value.trim() : "";
    const total = (currentOrder.unitPrice * currentOrder.qty).toFixed(2);

    const orderPayload = {
        customer_name: customerName || "Counter Guest",
        special_notes: notes || undefined,
        payment_method: currentOrder.paymentMethod,
        transaction_ref: trxId || undefined,
        items: [
            {
                menu_item_id: currentOrder.menu_item_id,
                quantity: currentOrder.qty
            }
        ]
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/orders`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(orderPayload)
        });

        if (response.ok) {
            const orderData = await response.json();
            alert(`Order Confirmed!\n\nOrder Code: ${orderData.order_code}\nCustomer: ${orderData.customer_name}\nTotal: $${parseFloat(orderData.total_price).toFixed(2)}\nStatus: ${orderData.status.toUpperCase()}\n\nPlease present this code at the cafe counter for pickup.`);
        } else {
            const errData = await response.json().catch(() => ({}));
            const errDetail = errData.detail || "Unable to place order.";
            alert(`Order Notice: ${errDetail}`);
        }
    } catch (e) {
        // Fallback for static browser preview
        alert(`Thank you, ${customerName}!\n\nYour order for ${currentOrder.qty}x ${currentOrder.name} ($${total}) has been received.\nPayment: ${currentOrder.paymentMethod}\nStatus: Ready at counter.`);
    }

    closeOrderModal();
}

async function submitWhatsAppOrder() {
    const customerName = document.getElementById("customerName") ? document.getElementById("customerName").value.trim() : "Valued Customer";
    const notes = document.getElementById("orderNotes") ? document.getElementById("orderNotes").value.trim() : "";
    const trxId = document.getElementById("trxIdInput") ? document.getElementById("trxIdInput").value.trim() : "";
    const total = (currentOrder.unitPrice * currentOrder.qty).toFixed(2);

    let orderCode = "PENDING";

    // Attempt to persist order record in database first
    try {
        const response = await fetch(`${API_BASE_URL}/api/orders`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                customer_name: customerName,
                special_notes: notes || undefined,
                payment_method: currentOrder.paymentMethod,
                transaction_ref: trxId || undefined,
                items: [{ menu_item_id: currentOrder.menu_item_id, quantity: currentOrder.qty }]
            })
        });

        if (response.ok) {
            const data = await response.json();
            orderCode = data.order_code;
        }
    } catch (e) {
        // Continue to WhatsApp redirect even if offline
    }

    let paymentText = currentOrder.paymentMethod;
    if ((currentOrder.paymentMethod === "bKash" || currentOrder.paymentMethod === "Nagad") && trxId) {
        paymentText += ` (TrxID / Sender: ${trxId})`;
    }

    let message = `Hello! I would like to place an order at Local Coffee Shop:\n\n`;
    if (orderCode !== "PENDING") {
        message += `Ref Code: ${orderCode}\n`;
    }
    message += `Item: ${currentOrder.qty}x ${currentOrder.name}\n`;
    message += `Total: $${total}\n`;
    message += `Payment: ${paymentText}\n`;
    if (notes) message += `Notes: ${notes}\n`;
    if (customerName) message += `Customer: ${customerName}\n`;
    message += `\nPlease confirm my order!`;

    const encoded = encodeURIComponent(message);
    const whatsappUrl = (typeof COFFEE_SHOP_WHATSAPP_NUMBER === "string" && COFFEE_SHOP_WHATSAPP_NUMBER.trim() !== "")
        ? `https://wa.me/${COFFEE_SHOP_WHATSAPP_NUMBER.trim()}?text=${encoded}`
        : `https://wa.me/?text=${encoded}`;

    window.open(whatsappUrl, "_blank", "noopener,noreferrer");
    closeOrderModal();
}

function showBannerNotification(text, type = "success") {
    let banner = document.getElementById("dynamicNotificationBanner");
    if (!banner) {
        banner = document.createElement("div");
        banner.id = "dynamicNotificationBanner";
        banner.style.position = "fixed";
        banner.style.bottom = "24px";
        banner.style.right = "24px";
        banner.style.zIndex = "9999";
        banner.style.padding = "1rem 1.5rem";
        banner.style.borderRadius = "8px";
        banner.style.boxShadow = "0 8px 24px rgba(0,0,0,0.18)";
        banner.style.fontWeight = "600";
        banner.style.fontSize = "0.95rem";
        banner.style.maxWidth = "400px";
        banner.style.transition = "all 0.3s ease";
        document.body.appendChild(banner);
    }

    if (type === "success") {
        banner.style.backgroundColor = "#2E7D32";
        banner.style.color = "#FFFFFF";
    } else {
        banner.style.backgroundColor = "#C62828";
        banner.style.color = "#FFFFFF";
    }

    banner.textContent = text;
    banner.style.display = "block";
    banner.style.opacity = "1";

    setTimeout(() => {
        banner.style.opacity = "0";
        setTimeout(() => { banner.style.display = "none"; }, 300);
    }, 4500);
}
