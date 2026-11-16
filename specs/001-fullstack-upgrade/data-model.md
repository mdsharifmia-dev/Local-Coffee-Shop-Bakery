# Data Models & Database Schema

Feature: specs/001-fullstack-upgrade
Date: 2026-11-16

## 1. Entity Relationship Diagram (Conceptual)

```
+--------------------+            +--------------------+
|     MenuItem       |            |       Order        |
+--------------------+            +--------------------+
| id (PK)            | 1        * | id (PK)            |
| name               |------------| order_code (UQ)    |
| category           |            | customer_name      |
| price              |            | customer_phone     |
| description        |            | special_notes      |
| is_available       |            | payment_method     |
| tag                |            | transaction_ref    |
| image_url          |            | total_price        |
| created_at         |            | status             |
+--------------------+            | created_at         |
                                  +--------------------+
                                            | 1
                                            |
                                            | *
                                  +--------------------+
                                  |     OrderItem      |
                                  +--------------------+
                                  | id (PK)            |
                                  | order_id (FK)      |
                                  | menu_item_id (FK)  |
                                  | item_name          |
                                  | unit_price         |
                                  | quantity           |
                                  | subtotal           |
                                  +--------------------+

+--------------------+
|   ContactMessage   |
+--------------------+
| id (PK)            |
| name               |
| email              |
| subject            |
| message            |
| created_at         |
+--------------------+
```

## 2. Relational Schemas (DDL Representation)

### Table: `menu_items`
```sql
CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    description TEXT,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    tag VARCHAR(50),
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_menu_category ON menu_items(category);
CREATE INDEX idx_menu_available ON menu_items(is_available);
```

### Table: `orders`
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_code VARCHAR(32) NOT NULL UNIQUE,
    customer_name VARCHAR(120) NOT NULL,
    customer_phone VARCHAR(30),
    special_notes TEXT,
    payment_method VARCHAR(50) NOT NULL,
    transaction_ref VARCHAR(100),
    total_price NUMERIC(10, 2) NOT NULL CHECK (total_price >= 0),
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_status ON orders(status);
```

### Table: `order_items`
```sql
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    menu_item_id INTEGER REFERENCES menu_items(id) ON DELETE SET NULL,
    item_name VARCHAR(120) NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    subtotal NUMERIC(10, 2) NOT NULL CHECK (subtotal >= 0)
);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

### Table: `contact_messages`
```sql
CREATE TABLE contact_messages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_contact_created_at ON contact_messages(created_at);
```
