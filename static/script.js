let cart = [];


// =====================================================
// NAVIGATION
// =====================================================

function scrollToMenu() {

    document.getElementById("menu").scrollIntoView({
        behavior: "smooth"
    });
}


function scrollToAI() {

    document.getElementById("ai").scrollIntoView({
        behavior: "smooth"
    });
}


// =====================================================
// TOAST
// =====================================================

function showToast(message) {

    const toast =
        document.getElementById("toast");

    toast.textContent = message;

    toast.classList.add("show");

    setTimeout(() => {

        toast.classList.remove("show");

    }, 2500);
}


// =====================================================
// ADD TO CART
// =====================================================

function addToCart(food) {

    const existingItem = cart.find(
        item => item.id === food.id
    );


    if (existingItem) {

        existingItem.quantity++;

    } else {

        cart.push({
            ...food,
            quantity: 1
        });
    }


    updateCart();

    showToast(
        `${food.name} added to cart 🛒`
    );
}


// =====================================================
// UPDATE CART
// =====================================================

function updateCart() {

    const cartCount =
        document.getElementById("cartCount");


    const totalItems = cart.reduce(
        (sum, item) =>
            sum + item.quantity,
        0
    );


    cartCount.textContent = totalItems;

    renderCart();
}


// =====================================================
// RENDER CART
// =====================================================

function renderCart() {

    const cartItems =
        document.getElementById("cartItems");

    const cartTotal =
        document.getElementById("cartTotal");


    if (!cartItems) return;


    cartItems.innerHTML = "";


    if (cart.length === 0) {

        cartItems.innerHTML = `

            <div class="empty-cart">

                <div class="empty-cart-icon">
                    🛒
                </div>

                <h3>
                    Your cart is empty
                </h3>

                <p>
                    Add something delicious from the menu.
                </p>

                <button
                    class="primary-btn"
                    onclick="closeCart(); scrollToMenu();"
                >
                    Browse Menu
                </button>

            </div>

        `;

        cartTotal.textContent = "₹0";

        return;
    }


    let total = 0;


    cart.forEach((item, index) => {

        const itemTotal =
            item.price * item.quantity;


        total += itemTotal;


        const cartItem =
            document.createElement("div");


        cartItem.className =
            "cart-item";


        cartItem.innerHTML = `

            <div class="cart-item-main">

                <div class="cart-item-icon">
                    ${item.emoji}
                </div>

                <div>

                    <h4>
                        ${item.name}
                    </h4>

                    <span>
                        ₹${item.price} each
                    </span>

                </div>

            </div>


            <div class="cart-item-controls">

                <button
                    onclick="decreaseQuantity(${index})"
                >
                    −
                </button>

                <strong>
                    ${item.quantity}
                </strong>

                <button
                    onclick="increaseQuantity(${index})"
                >
                    +
                </button>

            </div>


            <div class="cart-item-price">

                <strong>
                    ₹${itemTotal}
                </strong>

                <button
                    class="delete-btn"
                    onclick="removeFromCart(${index})"
                >
                    🗑️
                </button>

            </div>

        `;


        cartItems.appendChild(cartItem);

    });


    cartTotal.textContent =
        `₹${total}`;
}


// =====================================================
// QUANTITY
// =====================================================

function increaseQuantity(index) {

    cart[index].quantity++;

    updateCart();
}


function decreaseQuantity(index) {

    if (cart[index].quantity > 1) {

        cart[index].quantity--;

    } else {

        cart.splice(index, 1);
    }

    updateCart();
}


function removeFromCart(index) {

    const itemName =
        cart[index].name;

    cart.splice(index, 1);

    updateCart();

    showToast(
        `${itemName} removed`
    );
}


// =====================================================
// CART MODAL
// =====================================================

function openCart() {

    document
        .getElementById("cartModal")
        .classList.add("show");

    renderCart();
}


function closeCart() {

    document
        .getElementById("cartModal")
        .classList.remove("show");
}


window.addEventListener(
    "click",
    function(event) {

        const modal =
            document.getElementById("cartModal");

        if (event.target === modal) {

            closeCart();
        }
    }
);


// =====================================================
// PLACE ORDER
// =====================================================

function placeOrder() {

    if (cart.length === 0) {

        showToast(
            "Your cart is empty!"
        );

        return;
    }


    const orderId =
        "ZST" +
        Math.floor(
            100000 +
            Math.random() * 900000
        );


    const total =
        cart.reduce(
            (sum, item) =>
                sum +
                item.price *
                item.quantity,
            0
        );


    alert(
        `🎉 Order placed successfully!\n\n` +
        `Order ID: ${orderId}\n` +
        `Total: ₹${total}\n\n` +
        `Thank you for choosing Zestora!`
    );


    cart = [];

    updateCart();

    closeCart();
}


// =====================================================
// SEARCH
// =====================================================

function searchFoods() {

    const input =
        document.getElementById("searchInput");


    const searchTerm =
        input.value
            .toLowerCase()
            .trim();


    const cards =
        document.querySelectorAll(
            ".food-card"
        );


    let visibleCount = 0;


    cards.forEach(card => {

        const name =
            card.dataset.name
                .toLowerCase();


        const category =
            card.dataset.category
                .toLowerCase();


        const matches =
            name.includes(searchTerm) ||
            category.includes(searchTerm);


        card.style.display =
            matches ? "block" : "none";


        if (matches) {

            visibleCount++;
        }

    });


    document.getElementById(
        "noResults"
    ).style.display =
        visibleCount === 0
            ? "block"
            : "none";
}


// =====================================================
// CATEGORY FILTER
// =====================================================

function filterFoods(
    category,
    button
) {

    const cards =
        document.querySelectorAll(
            ".food-card"
        );


    const buttons =
        document.querySelectorAll(
            ".category-btn"
        );


    buttons.forEach(btn => {

        btn.classList.remove(
            "active"
        );
    });


    if (button) {

        button.classList.add(
            "active"
        );
    }


    document.getElementById(
        "searchInput"
    ).value = "";


    let visibleCount = 0;


    cards.forEach(card => {

        const cardCategory =
            card.dataset.category;


        const matches =
            category === "All" ||
            cardCategory === category;


        card.style.display =
            matches ? "block" : "none";


        if (matches) {

            visibleCount++;
        }

    });


    document.getElementById(
        "noResults"
    ).style.display =
        visibleCount === 0
            ? "block"
            : "none";
}


// =====================================================
// AI QUICK PROMPTS
// =====================================================

function usePrompt(prompt) {

    document.getElementById(
        "aiInput"
    ).value = prompt;

    askAI();
}


// =====================================================
// AI CHAT
// =====================================================

async function askAI() {

    const input =
        document.getElementById(
            "aiInput"
        );


    const responseBox =
        document.getElementById(
            "aiResponse"
        );


    const button =
        document.getElementById(
            "aiButton"
        );


    const message =
        input.value.trim();


    if (!message) {

        showToast(
            "Please enter a question."
        );

        return;
    }


    responseBox.innerHTML = `

        <div class="ai-loading">

            🤖

            <span>
                Zestora AI is thinking...
            </span>

        </div>

    `;


    button.disabled = true;

    button.textContent =
        "Thinking...";


    try {

        const response =
            await fetch(
                "/api/ai",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        const data =
            await response.json();


        if (response.ok) {

            responseBox.innerHTML =
                formatAIResponse(
                    data.response
                );

        } else {

            responseBox.innerHTML = `

                <span class="error-text">

                    ⚠️
                    ${data.response ||
                    "Something went wrong."}

                </span>

            `;
        }


    } catch (error) {

        console.error(error);


        responseBox.innerHTML = `

            <span class="error-text">

                ⚠️ Unable to connect
                to Zestora AI.

            </span>

        `;

    } finally {

        button.disabled = false;

        button.textContent =
            "Ask AI";
    }
}


// =====================================================
// FORMAT AI RESPONSE
// =====================================================

function formatAIResponse(text) {

    return text
        .replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        )
        .replace(
            /\n/g,
            "<br>"
        );
}


// =====================================================
// ENTER KEY
// =====================================================

function handleAIKey(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        askAI();
    }
}


// =====================================================
// INITIALIZE
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        updateCart();

    }
);