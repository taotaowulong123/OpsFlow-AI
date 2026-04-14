-- OpsFlow AI Demo Data: E-commerce Mock Database
-- This SQL file creates mock tables and data for the demo scenario

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2),
    stock_quantity INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_no VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(100),
    product_id INT REFERENCES products(id),
    quantity INT DEFAULT 1,
    total_amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS refunds (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    reason_code VARCHAR(10),
    reason_desc VARCHAR(200),
    amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS work_orders (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    description TEXT,
    priority VARCHAR(10) DEFAULT 'P2',
    status VARCHAR(20) DEFAULT 'open',
    assignee VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);

-- Insert demo products
INSERT INTO products (name, category, price, stock_quantity, status) VALUES
('无线蓝牙耳机 Pro', '数码配件', 299.00, 500, 'active'),
('智能手表 S3', '智能穿戴', 899.00, 200, 'active'),
('便携充电宝 20000mAh', '数码配件', 159.00, 800, 'active'),
('机械键盘 K8', '电脑外设', 459.00, 300, 'active'),
('USB-C 扩展坞', '电脑外设', 239.00, 150, 'active'),
('降噪耳机 ANC-100', '数码配件', 599.00, 100, 'active'),
('平板支架 铝合金版', '配件', 89.00, 1000, 'active'),
('Type-C 数据线 3条装', '配件', 39.00, 2000, 'active');

-- Insert demo orders (last 30 days)
INSERT INTO orders (order_no, customer_name, product_id, quantity, total_amount, status, created_at) VALUES
('ORD-20250401-001', '张三', 1, 1, 299.00, 'completed', NOW() - INTERVAL '14 days'),
('ORD-20250401-002', '李四', 2, 1, 899.00, 'completed', NOW() - INTERVAL '14 days'),
('ORD-20250402-001', '王五', 1, 2, 598.00, 'completed', NOW() - INTERVAL '13 days'),
('ORD-20250402-002', '赵六', 3, 1, 159.00, 'completed', NOW() - INTERVAL '13 days'),
('ORD-20250403-001', '钱七', 4, 1, 459.00, 'completed', NOW() - INTERVAL '12 days'),
('ORD-20250403-002', '孙八', 1, 1, 299.00, 'completed', NOW() - INTERVAL '12 days'),
('ORD-20250404-001', '周九', 5, 1, 239.00, 'completed', NOW() - INTERVAL '11 days'),
('ORD-20250404-002', '吴十', 6, 1, 599.00, 'completed', NOW() - INTERVAL '11 days'),
('ORD-20250405-001', '郑一', 1, 1, 299.00, 'completed', NOW() - INTERVAL '10 days'),
('ORD-20250405-002', '冯二', 2, 1, 899.00, 'completed', NOW() - INTERVAL '10 days'),
('ORD-20250406-001', '陈三', 7, 2, 178.00, 'completed', NOW() - INTERVAL '9 days'),
('ORD-20250406-002', '褚四', 1, 1, 299.00, 'completed', NOW() - INTERVAL '9 days'),
('ORD-20250407-001', '卫五', 3, 1, 159.00, 'completed', NOW() - INTERVAL '8 days'),
('ORD-20250407-002', '蒋六', 8, 3, 117.00, 'completed', NOW() - INTERVAL '8 days'),
('ORD-20250408-001', '沈七', 1, 1, 299.00, 'completed', NOW() - INTERVAL '7 days'),
('ORD-20250408-002', '韩八', 4, 1, 459.00, 'completed', NOW() - INTERVAL '7 days'),
('ORD-20250409-001', '杨九', 6, 1, 599.00, 'completed', NOW() - INTERVAL '6 days'),
('ORD-20250409-002', '朱十', 1, 1, 299.00, 'completed', NOW() - INTERVAL '6 days'),
('ORD-20250410-001', '秦一', 2, 1, 899.00, 'completed', NOW() - INTERVAL '5 days'),
('ORD-20250410-002', '尤二', 5, 1, 239.00, 'completed', NOW() - INTERVAL '5 days'),
('ORD-20250411-001', '许三', 1, 2, 598.00, 'completed', NOW() - INTERVAL '4 days'),
('ORD-20250411-002', '何四', 3, 1, 159.00, 'completed', NOW() - INTERVAL '4 days'),
('ORD-20250412-001', '吕五', 6, 1, 599.00, 'completed', NOW() - INTERVAL '3 days'),
('ORD-20250412-002', '施六', 1, 1, 299.00, 'completed', NOW() - INTERVAL '3 days'),
('ORD-20250413-001', '张七', 4, 1, 459.00, 'completed', NOW() - INTERVAL '2 days'),
('ORD-20250413-002', '孔八', 2, 1, 899.00, 'completed', NOW() - INTERVAL '2 days'),
('ORD-20250414-001', '曹九', 1, 1, 299.00, 'completed', NOW() - INTERVAL '1 day'),
('ORD-20250414-002', '严十', 7, 1, 89.00, 'completed', NOW() - INTERVAL '1 day');

-- Insert demo refunds (simulate abnormal refund rate for product 1)
INSERT INTO refunds (order_id, product_id, reason_code, reason_desc, amount, status, created_at) VALUES
(1, 1, 'R001', '耳机左声道无声', 299.00, 'approved', NOW() - INTERVAL '13 days'),
(3, 1, 'R001', '连接不稳定频繁断连', 598.00, 'approved', NOW() - INTERVAL '12 days'),
(6, 1, 'R002', '实际颜色与图片不符', 299.00, 'approved', NOW() - INTERVAL '11 days'),
(9, 1, 'R001', '充电仓无法充电', 299.00, 'approved', NOW() - INTERVAL '9 days'),
(12, 1, 'R001', '佩戴不到一周耳机开裂', 299.00, 'pending', NOW() - INTERVAL '8 days'),
(15, 1, 'R004', '音质不如预期', 299.00, 'approved', NOW() - INTERVAL '6 days'),
(18, 1, 'R001', '右耳机无法开机', 299.00, 'pending', NOW() - INTERVAL '5 days'),
(24, 1, 'R002', '包装破损配件缺失', 299.00, 'pending', NOW() - INTERVAL '2 days'),
(27, 1, 'R001', '蓝牙配对失败', 299.00, 'pending', NOW() - INTERVAL '1 day'),
(2, 2, 'R003', '快递运输导致屏幕碎裂', 899.00, 'approved', NOW() - INTERVAL '13 days'),
(8, 6, 'R004', '降噪效果不明显', 599.00, 'approved', NOW() - INTERVAL '10 days'),
(17, 6, 'R001', '头梁断裂', 599.00, 'pending', NOW() - INTERVAL '5 days');
