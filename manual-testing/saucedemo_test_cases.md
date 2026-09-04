# Sauce Demo — Manual Test Case Suite

**Application Under Test:** https://www.saucedemo.com/
**Tester:** Heidi
**Test Accounts:** standard_user, locked_out_user, problem_user, performance_glitch_user, error_user, visual_user (all password: `secret_sauce`)

---

## Section 1: Login

| Test ID | Title | Preconditions | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| TC_LOGIN_001 | Valid login with standard_user | On login page | 1. Enter username "standard_user" 2. Enter password "secret_sauce" 3. Click Login | Redirected to Products page | High |
| TC_NEGATIVE_001 | Login with blank password | On login page | 1. Enter username "standard_user" 2. Leave password blank 3. Click Login | Error: "Password is required"; stays on login page | High |
| TC_NEGATIVE_002 | Login with blank username | On login page | 1. Leave username blank 2. Enter password "secret_sauce" 3. Click Login | Error: "Username is required"; stays on login page | High |
| TC_NEGATIVE_003 | Login with both fields blank | On login page | 1. Leave username blank 2. Leave password blank 3. Click Login | Error: "Username is required" (username error takes priority when both fields are blank) | High |
| TC_NEGATIVE_004 | Login with invalid username/password combo | On login page | 1. Enter username "wrong_user" 2. Enter password "wrong_pass" 3. Click Login | Error: "Username and password do not match any user in this service" | High |
| TC_NEGATIVE_005 | Login with valid username, wrong password | On login page | 1. Enter username "standard_user" 2. Enter password "wrong_pass" 3. Click Login | Error: "Username and password do not match any user in this service" | High |
| TC_LOCKED_OUT_001 | Login attempt with locked-out account | On login page | 1. Enter username "locked_out_user" 2. Enter password "secret_sauce" 3. Click Login | Error: "Sorry, this user has been locked out." | High |
| TC_LOGIN_002 | Password field masks input | On login page | 1. Click password field 2. Type "secret_sauce" | Input displayed as dots/asterisks, not plain text | Medium |
| TC_LOGIN_003 | Login with leading/trailing whitespace in username | On login page | 1. Enter username " standard_user " (with spaces) 2. Enter valid password 3. Click Login | *Assumption: system should trim whitespace or reject cleanly — document actual behavior* | Low |
| TC_LOGIN_004 | Case sensitivity of username | On login page | 1. Enter username "STANDARD_USER" 2. Enter password "secret_sauce" 3. Click Login | *Assumption: usernames are case-sensitive → should fail; document actual behavior* | Low |
| TC_LOGIN_005 | SQL injection attempt in username field | On login page | 1. Enter username `' OR '1'='1` 2. Enter any password 3. Click Login | Login rejected; no unexpected access or error exposing system internals | High |
| TC_LOGIN_006 | Login with performance_glitch_user | On login page | 1. Enter username "performance_glitch_user" 2. Enter password "secret_sauce" 3. Click Login | Redirected to Products page (may load slowly — note load time observed) | Low |

---

## Section 2: Product Listing Page

| Test ID | Title | Preconditions | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| TC_PRODUCTS_001 | Product page loads all items | Logged in as standard_user | 1. Observe Products page | All 6 products display with name, image, price, and "Add to cart" button | High |
| TC_PRODUCTS_002 | Sort products by Name (A–Z) | On Products page | 1. Open sort dropdown 2. Select "Name (A to Z)" | Products reorder alphabetically ascending | Medium |
| TC_PRODUCTS_003 | Sort products by Name (Z–A) | On Products page | 1. Open sort dropdown 2. Select "Name (Z to A)" | Products reorder alphabetically descending | Medium |
| TC_PRODUCTS_004 | Sort products by Price (low–high) | On Products page | 1. Open sort dropdown 2. Select "Price (low to high)" | Products reorder by ascending price | Medium |
| TC_PRODUCTS_005 | Sort products by Price (high–low) | On Products page | 1. Open sort dropdown 2. Select "Price (high to low)" | Products reorder by descending price | Medium |
| TC_PRODUCTS_006 | Add single item to cart | On Products page | 1. Click "Add to cart" on any item | Button changes to "Remove"; cart icon shows count "1" | High |
| TC_PRODUCTS_007 | Remove item from cart via Products page | Item already added | 1. Click "Remove" on the added item | Button reverts to "Add to cart"; cart count decreases | High |
| TC_PRODUCTS_008 | Add all items to cart | On Products page | 1. Click "Add to cart" on all 6 products | Cart icon shows count "6"; all buttons show "Remove" | Medium |
| TC_PRODUCTS_009 | Click product name to view details | On Products page | 1. Click a product's name/title | Redirected to that product's detail page with matching name, description, price | Medium |
| TC_PRODUCTS_010 | Cart badge does not appear when cart is empty | Fresh login, no items added | 1. Observe cart icon | No numeric badge shown on cart icon | Low |

---

## Section 3: Cart

| Test ID | Title | Preconditions | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| TC_CART_001 | View cart with items added | 2 items added to cart | 1. Click cart icon | Cart page lists both items with correct name, price, and quantity | High |
| TC_CART_002 | Remove item from cart page | On cart page with items | 1. Click "Remove" next to an item | Item disappears from cart list; cart count updates | High |
| TC_CART_003 | Continue Shopping button | On cart page | 1. Click "Continue Shopping" | Redirected back to Products page, cart contents preserved | Medium |
| TC_BOUNDARY_002 | Checkout with 0 items in cart | Logged in, cart empty | 1. Click cart icon 2. Click "Checkout" (if available) | *Bug found: system allows checkout and completes order with 0 items — should block with a validation message* | High |
| TC_BOUNDARY_003 | Checkout with 1 item in cart | Logged in, 1 item in cart | 1. Click cart icon 2. Click "Checkout" | Redirected to checkout information page | High |

---

## Section 4: Checkout — Your Information

| Test ID | Title | Preconditions | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| TC_CHECKOUT_001 | Complete checkout info with valid data | On checkout-step-one, cart has items | 1. Enter First Name 2. Enter Last Name 3. Enter Zip Code 4. Click Continue | Redirected to checkout overview page | High |
| TC_CHECKOUT_002 | Submit with blank First Name | On checkout-step-one | 1. Leave First Name blank 2. Fill Last Name and Zip 3. Click Continue | Error: "First Name is required" | High |
| TC_CHECKOUT_003 | Submit with blank Last Name | On checkout-step-one | 1. Fill First Name 2. Leave Last Name blank 3. Fill Zip 4. Click Continue | Error: "Last Name is required" | High |
| TC_CHECKOUT_004 | Submit with blank Zip Code | On checkout-step-one | 1. Fill First Name and Last Name 2. Leave Zip blank 3. Click Continue | Error: "Postal Code is required" | High |
| TC_CHECKOUT_005 | Submit with all fields blank | On checkout-step-one | 1. Leave all fields blank 2. Click Continue | Error shown for first required field (First Name) | Medium |
| TC_BOUNDARY_001 | Zip code field accepts invalid length (20 characters) | On checkout-step-one, Name fields filled | 1. Enter 20-character string in Zip field 2. Click Continue | *Bug found: no validation error shown; user proceeds to overview page despite invalid zip format* | High |
| TC_CHECKOUT_006 | Cancel button on checkout info page | On checkout-step-one | 1. Click "Cancel" | Redirected back to Products page or cart, cart contents preserved | Low |

---

## Section 5: Checkout — Overview & Completion

| Test ID | Title | Preconditions | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| TC_OVERVIEW_001 | Overview page displays correct item summary | On checkout-step-two | 1. Observe item list, quantities, prices | All items match what was in cart; subtotal, tax, and total calculated correctly | High |
| TC_OVERVIEW_002 | Tax calculation accuracy | On checkout-step-two | 1. Manually calculate expected tax on subtotal 2. Compare to displayed tax | Displayed tax matches expected calculation | Medium |
| TC_OVERVIEW_003 | Finish button completes order | On checkout-step-two | 1. Click "Finish" | Redirected to confirmation page: "Thank you for your order!" | High |
| TC_OVERVIEW_004 | Cancel button on overview page | On checkout-step-two | 1. Click "Cancel" | Redirected to Products page, order not placed | Medium |
| TC_OVERVIEW_005 | Cart is emptied after successful order | Order just completed | 1. Click cart icon after confirmation | Cart shows 0 items | High |
| TC_OVERVIEW_006 | Back to Products button on confirmation page | On order confirmation page | 1. Click "Back Home" | Redirected to Products page | Low |

---

## Section 6: Cross-cutting / Session

| Test ID | Title | Preconditions | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| TC_SESSION_001 | Logout functionality | Logged in | 1. Open side menu 2. Click "Logout" | Redirected to login page; session ended | High |
| TC_SESSION_002 | Access Products page directly via URL after logout | Logged out | 1. Navigate directly to /inventory.html | User is redirected to login page, not allowed direct access | High |
| TC_SESSION_003 | Cart contents persist across page navigation | Items in cart | 1. Add items 2. Navigate to product detail page and back | Cart count and contents remain unchanged | Medium |
| TC_UI_001 | Reset App State function | Logged in, items in cart | 1. Open side menu 2. Click "Reset App State" | Cart is emptied; any "Remove" buttons revert to "Add to cart" | Low |

---

## Known Bugs Found During Testing

1. **[High] Empty cart checkout allowed** — System permits full checkout and order completion with 0 items in cart, including a confirmation message and receipt. (Ref: TC_BOUNDARY_002)
2. **[High] Zip code field lacks validation** — Field accepts 20+ character input with no format/length validation, proceeding straight to checkout overview. (Ref: TC_BOUNDARY_001)
3. **[Low/Cosmetic] Error "x" indicator on unrelated fields** — On failed login attempts, an "x" error indicator appears on both username and password fields even when only one field is invalid (e.g., valid username, blank password still shows "x" on username). (Ref: TC_NEGATIVE_001, TC_LOCKED_OUT_001)

---

*Total: 34 test cases across Login, Product Listing, Cart, Checkout Info, Checkout Overview, and Session/Cross-cutting flows.*
