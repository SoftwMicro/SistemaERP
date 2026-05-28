CREATE TABLE `orders_cliente` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cpf_cnpj` varchar(18) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `endereco` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `ativo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cpf_cnpj` (`cpf_cnpj`),
  UNIQUE KEY `email` (`email`),
  KEY `orders_clie_email_b88daa_idx` (`email`),
  KEY `orders_clie_cpf_cnp_0181e8_idx` (`cpf_cnpj`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- pedidos.orders_produto definição

CREATE TABLE `orders_produto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sku` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nome` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descricao` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `preco` decimal(10,2) NOT NULL,
  `quantidade_estoque` int unsigned NOT NULL,
  `ativo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`),
  KEY `orders_prod_sku_899940_idx` (`sku`),
  KEY `orders_prod_nome_db78f2_idx` (`nome`),
  CONSTRAINT `orders_produto_chk_1` CHECK ((`quantidade_estoque` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- pedidos.orders_order definição

CREATE TABLE `orders_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `data_criacao` datetime(6) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `valor_total` decimal(12,2) NOT NULL,
  `observacoes` longtext COLLATE utf8mb4_unicode_ci,
  `cliente_id` bigint NOT NULL,
  `idempotency_key` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idempotency_key` (`idempotency_key`),
  KEY `orders_orde_status_c6dd84_idx` (`status`),
  KEY `orders_orde_data_cr_c26e42_idx` (`data_criacao`),
  KEY `orders_order_cliente_id_0fda56df_fk_orders_cliente_id` (`cliente_id`),
  KEY `orders_order_status_445594e5` (`status`),
  CONSTRAINT `orders_order_cliente_id_0fda56df_fk_orders_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `orders_cliente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- pedidos.orders_orderitem definição

CREATE TABLE `orders_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantidade` int unsigned NOT NULL,
  `preco_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `pedido_id` bigint NOT NULL,
  `produto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `orders_orderitem_pedido_id_produto_id_49792a69_uniq` (`pedido_id`,`produto_id`),
  KEY `orders_orderitem_produto_id_e7ecb994_fk_orders_produto_id` (`produto_id`),
  CONSTRAINT `orders_orderitem_pedido_id_beba6869_fk_orders_order_id` FOREIGN KEY (`pedido_id`) REFERENCES `orders_order` (`id`),
  CONSTRAINT `orders_orderitem_produto_id_e7ecb994_fk_orders_produto_id` FOREIGN KEY (`produto_id`) REFERENCES `orders_produto` (`id`),
  CONSTRAINT `orders_orderitem_chk_1` CHECK ((`quantidade` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- pedidos.orders_orderstatushistory definição

CREATE TABLE `orders_orderstatushistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `data_hora` datetime(6) NOT NULL,
  `status_anterior` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `novo_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usuario` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `observacoes` longtext COLLATE utf8mb4_unicode_ci,
  `pedido_id` bigint NOT NULL,
  `idempotency_key` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_orderstatushistory_pedido_id_505f7081_fk_orders_order_id` (`pedido_id`),
  KEY `orders_orderstatushistory_idempotency_key_bd476005` (`idempotency_key`),
  CONSTRAINT `orders_orderstatushistory_pedido_id_505f7081_fk_orders_order_id` FOREIGN KEY (`pedido_id`) REFERENCES `orders_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;