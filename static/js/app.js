/**
 * AirMenu - Main Application
 * Handles screens, cart, and interactions
 */

class AirMenuApp {
      constructor() {
            this.handTracker = null;
            this.menuData = null;
            this.currentScreen = 'home';
            this.currentCategory = null;
            this.cart = [];
            this.config = {
                  currencySymbol: '₹',
                  gstRate: 0.18,
                  restaurantName: 'AirMenu Restaurant'
            };

            // Dwell selection
            this.hoveredElement = null;
            this.hoverStartTime = null;
            this.dwellTime = 800; // ms
            this.interactionCooldown = 300;
            this.lastInteractionTime = 0;
      }

      async init() {
            // Load menu data
            try {
                  const response = await fetch('/api/menu');
                  this.menuData = await response.json();
                  this.config = { ...this.config, ...this.menuData.config };
            } catch (error) {
                  console.error('Failed to load menu:', error);
            }

            // Initialize hand tracker
            this.handTracker = new HandTracker();
            this.handTracker.onHandUpdate = (pos, isPinching) => this.handleHandUpdate(pos, isPinching);
            this.handTracker.onPinch = (pos) => this.handlePinch(pos);
            await this.handTracker.init();

            // Setup event listeners for buttons
            this.setupEventListeners();

            // Render categories
            this.renderCategories();

            // Start update loop
            this.update();
      }

      setupEventListeners() {
            // Add click events as fallback for mouse/touch
            document.querySelectorAll('[data-action]').forEach(btn => {
                  btn.addEventListener('click', (e) => {
                        this.handleAction(btn.dataset.action, btn);
                  });
            });
      }

      handleAction(action, element) {
            const now = Date.now();
            if (now - this.lastInteractionTime < this.interactionCooldown) return;
            this.lastInteractionTime = now;

            switch (action) {
                  case 'start-ordering':
                        this.showScreen('category');
                        break;
                  case 'go-home':
                        this.showScreen('home');
                        break;
                  case 'go-categories':
                        this.showScreen('category');
                        break;
                  case 'go-cart':
                        this.showScreen('cart');
                        this.renderCart();
                        break;
                  case 'select-category':
                        this.currentCategory = element.dataset.category;
                        this.renderItems(this.currentCategory);
                        this.showScreen('items');
                        break;
                  case 'add-item':
                        this.addToCart(parseInt(element.dataset.itemId));
                        break;
                  case 'increase-qty':
                        this.updateQuantity(parseInt(element.dataset.itemId), 1);
                        break;
                  case 'decrease-qty':
                        this.updateQuantity(parseInt(element.dataset.itemId), -1);
                        break;
                  case 'checkout':
                        this.checkout();
                        break;
                  case 'new-order':
                        this.cart = [];
                        this.updateCartCount();
                        this.showScreen('home');
                        break;
            }
      }

      showScreen(screenName) {
            // Hide all screens
            document.querySelectorAll('.screen').forEach(screen => {
                  screen.classList.remove('active');
                  screen.classList.add('exiting');
            });

            // Show target screen
            setTimeout(() => {
                  document.querySelectorAll('.screen').forEach(screen => {
                        screen.classList.remove('exiting');
                  });
                  document.getElementById(`${screenName}-screen`).classList.add('active');
                  this.currentScreen = screenName;
            }, 100);
      }

      renderCategories() {
            const grid = document.getElementById('categories-grid');
            grid.innerHTML = '';

            this.menuData.categories.forEach(category => {
                  const card = document.createElement('div');
                  card.className = 'glass-card category-card';
                  card.dataset.action = 'select-category';
                  card.dataset.category = category.id;
                  card.innerHTML = `
                <div class="category-icon">${category.icon}</div>
                <div class="category-name">${category.name}</div>
                <div class="dwell-progress"></div>
            `;
                  card.addEventListener('click', () => this.handleAction('select-category', card));
                  grid.appendChild(card);
            });
      }

      renderItems(categoryId) {
            const list = document.getElementById('items-list');
            const title = document.getElementById('items-title');

            const category = this.menuData.categories.find(c => c.id === categoryId);
            title.textContent = category ? category.name : 'Menu Items';

            const items = this.menuData.items.filter(item => item.category === categoryId);

            list.innerHTML = '';
            items.forEach(item => {
                  const card = document.createElement('div');
                  card.className = 'glass-card item-card';
                  card.innerHTML = `
                <div class="item-info">
                    <div class="item-name">${item.name}</div>
                    <div class="item-desc">${item.description}</div>
                </div>
                <div class="item-price">${this.config.currencySymbol}${item.price}</div>
                <button class="glass-button add-btn" data-action="add-item" data-item-id="${item.id}">
                    +
                    <div class="dwell-progress"></div>
                </button>
            `;
                  card.querySelector('.add-btn').addEventListener('click', (e) => {
                        e.stopPropagation();
                        this.handleAction('add-item', e.currentTarget);
                  });
                  list.appendChild(card);
            });
      }

      addToCart(itemId) {
            const item = this.menuData.items.find(i => i.id === itemId);
            if (!item) return;

            const existing = this.cart.find(c => c.id === itemId);
            if (existing) {
                  existing.quantity++;
            } else {
                  this.cart.push({ ...item, quantity: 1 });
            }

            this.updateCartCount();
            this.showAddedFeedback(itemId);
      }

      showAddedFeedback(itemId) {
            const btn = document.querySelector(`[data-item-id="${itemId}"]`);
            if (btn) {
                  btn.textContent = '✓';
                  btn.style.background = 'var(--success)';
                  setTimeout(() => {
                        btn.innerHTML = '+<div class="dwell-progress"></div>';
                        btn.style.background = '';
                  }, 500);
            }
      }

      updateQuantity(itemId, delta) {
            const item = this.cart.find(c => c.id === itemId);
            if (!item) return;

            item.quantity += delta;
            if (item.quantity <= 0) {
                  this.cart = this.cart.filter(c => c.id !== itemId);
            }

            this.updateCartCount();
            this.renderCart();
      }

      updateCartCount() {
            const count = this.cart.reduce((sum, item) => sum + item.quantity, 0);
            document.querySelectorAll('.cart-count').forEach(el => {
                  el.textContent = count;
            });
      }

      renderCart() {
            const cartItems = document.getElementById('cart-items');
            const cartContent = document.getElementById('cart-content');
            const cartEmpty = document.getElementById('cart-empty');

            if (this.cart.length === 0) {
                  cartContent.classList.add('hidden');
                  cartEmpty.classList.add('show');
                  return;
            }

            cartContent.classList.remove('hidden');
            cartEmpty.classList.remove('show');

            cartItems.innerHTML = '';
            this.cart.forEach(item => {
                  const div = document.createElement('div');
                  div.className = 'glass-card cart-item';
                  div.innerHTML = `
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">${this.config.currencySymbol}${item.price} each</div>
                </div>
                <div class="quantity-controls">
                    <button class="glass-button qty-btn" data-action="decrease-qty" data-item-id="${item.id}">
                        −
                        <div class="dwell-progress"></div>
                    </button>
                    <span class="quantity">${item.quantity}</span>
                    <button class="glass-button qty-btn" data-action="increase-qty" data-item-id="${item.id}">
                        +
                        <div class="dwell-progress"></div>
                    </button>
                </div>
                <div class="cart-item-total">${this.config.currencySymbol}${item.price * item.quantity}</div>
            `;

                  div.querySelectorAll('[data-action]').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                              e.stopPropagation();
                              this.handleAction(btn.dataset.action, btn);
                        });
                  });

                  cartItems.appendChild(div);
            });

            this.updateSummary();
      }

      updateSummary() {
            const subtotal = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            const gst = Math.round(subtotal * this.config.gstRate);
            const total = subtotal + gst;

            document.getElementById('subtotal').textContent = `${this.config.currencySymbol}${subtotal}`;
            document.getElementById('gst').textContent = `${this.config.currencySymbol}${gst}`;
            document.getElementById('total').textContent = `${this.config.currencySymbol}${total}`;
      }

      checkout() {
            if (this.cart.length === 0) return;

            // Generate order ID
            const orderId = Math.floor(1000 + Math.random() * 9000);
            document.getElementById('order-id').textContent = orderId;

            // Render receipt items
            const receiptItems = document.getElementById('receipt-items');
            receiptItems.innerHTML = '';
            this.cart.forEach(item => {
                  const div = document.createElement('div');
                  div.className = 'receipt-item';
                  div.innerHTML = `
                <span>${item.name} x${item.quantity}</span>
                <span>${this.config.currencySymbol}${item.price * item.quantity}</span>
            `;
                  receiptItems.appendChild(div);
            });

            // Update receipt totals
            const subtotal = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            const gst = Math.round(subtotal * this.config.gstRate);
            const total = subtotal + gst;

            document.getElementById('receipt-subtotal').textContent = `${this.config.currencySymbol}${subtotal}`;
            document.getElementById('receipt-gst').textContent = `${this.config.currencySymbol}${gst}`;
            document.getElementById('receipt-total').textContent = `${this.config.currencySymbol}${total}`;

            this.showScreen('receipt');
      }

      handleHandUpdate(pos, isPinching) {
            if (!pos) {
                  this.clearHover();
                  return;
            }

            // Find element under cursor
            const element = this.getInteractiveElementAt(pos.x, pos.y);

            if (element) {
                  if (element !== this.hoveredElement) {
                        this.clearHover();
                        this.hoveredElement = element;
                        this.hoverStartTime = Date.now();
                        element.classList.add('hovered');
                  }

                  // Check dwell time
                  const elapsed = Date.now() - this.hoverStartTime;
                  const progress = Math.min(elapsed / this.dwellTime, 1);

                  // Update dwell progress
                  const progressBar = element.querySelector('.dwell-progress');
                  if (progressBar) {
                        progressBar.style.width = `${progress * 100}%`;
                  }

                  if (elapsed >= this.dwellTime) {
                        element.classList.add('dwelling');
                  }

                  // Dwell activation
                  if (elapsed >= this.dwellTime && Date.now() - this.lastInteractionTime > this.interactionCooldown) {
                        this.activateElement(element);
                  }
            } else {
                  this.clearHover();
            }
      }

      handlePinch(pos) {
            const element = this.getInteractiveElementAt(pos.x, pos.y);
            if (element && Date.now() - this.lastInteractionTime > this.interactionCooldown) {
                  this.activateElement(element);
            }
      }

      getInteractiveElementAt(x, y) {
            const elements = document.elementsFromPoint(x, y);
            return elements.find(el =>
                  el.classList.contains('glass-button') ||
                  el.classList.contains('category-card') ||
                  el.dataset.action
            );
      }

      activateElement(element) {
            this.lastInteractionTime = Date.now();
            this.clearHover();

            const action = element.dataset.action;
            if (action) {
                  this.handleAction(action, element);
            }
      }

      clearHover() {
            if (this.hoveredElement) {
                  this.hoveredElement.classList.remove('hovered', 'dwelling');
                  const progressBar = this.hoveredElement.querySelector('.dwell-progress');
                  if (progressBar) {
                        progressBar.style.width = '0%';
                  }
                  this.hoveredElement = null;
                  this.hoverStartTime = null;
            }
      }

      update() {
            requestAnimationFrame(() => this.update());
      }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
      const app = new AirMenuApp();
      app.init();
});
