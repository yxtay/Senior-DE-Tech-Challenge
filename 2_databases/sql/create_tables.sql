-- Creation of users table
CREATE TABLE IF NOT EXISTS users (
  user_id VARCHAR(250) NOT NULL,
  user_name VARCHAR(250) NOT NULL,
  first_name VARCHAR(250) NOT NULL,
  last_name VARCHAR(250) NOT NULL,
  date_of_birth date NOT NULL,
  PRIMARY KEY (user_id)
);

-- Creation of merchants table
CREATE TABLE IF NOT EXISTS merchants (
  merchant_id UUID NOT NULL DEFAULT gen_random_uuid(),
  merchant_name VARCHAR(250) NOT NULL,
  PRIMARY KEY (merchant_id)
);

-- Creation of products table
CREATE TABLE IF NOT EXISTS products (
  product_id UUID NOT NULL DEFAULT gen_random_uuid(),
  product_name VARCHAR(250) NOT NULL,
  cost NUMERIC NOT NULL,
  weight NUMERIC NOT NULL,
  merchant_id UUID NOT NULL, 
  PRIMARY KEY (product_id),
  CONSTRAINT fk_merchant
      FOREIGN KEY(merchant_id) 
	  REFERENCES merchants(merchant_id)	
);

-- Creation of orders table
CREATE TABLE IF NOT EXISTS orders (
  order_id UUID NOT NULL DEFAULT gen_random_uuid(),
  order_datetime TIMESTAMP NOT NULL,
  total_price NUMERIC NOT NULL,
  total_weight NUMERIC NOT NULL,
  user_id VARCHAR(250) NOT NULL,
  PRIMARY KEY (order_id),
  CONSTRAINT fk_user
      FOREIGN KEY(user_id) 
	  REFERENCES users(user_id)
);

-- Creation of order items table
CREATE TABLE IF NOT EXISTS order_details (
  order_detail_id UUID NOT NULL DEFAULT gen_random_uuid(),
  quantity NUMERIC NOT NULL,
  price NUMERIC NOT NULL,
  weight NUMERIC NOT NULL,
  order_id UUID NOT NULL,
  product_id UUID NOT NULL,
  PRIMARY KEY (order_detail_id),
  CONSTRAINT fk_order
      FOREIGN KEY(order_id) 
	  REFERENCES orders(order_id), 
  CONSTRAINT fk_product
      FOREIGN KEY(product_id) 
	  REFERENCES products(product_id)
);
