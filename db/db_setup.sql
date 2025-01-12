CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,                             -- Unique ID for user
    username VARCHAR(255) NOT NULL UNIQUE,                            -- Unique username
    email VARCHAR(255) NOT NULL UNIQUE,                               -- Unique email
    password_hash VARCHAR(255) NOT NULL,                              -- Password hash for auth
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                   -- Account creation time
    last_login TIMESTAMP                                              -- Tracks user's last login
);

CREATE TABLE messages (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,                             -- Unique ID
    sender_id BIGINT NOT NULL,                                        -- Sender's ID
    receiver_id BIGINT NOT NULL,                                      -- Reciever's ID
    message TEXT NOT NULL,                                            -- Message content
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                    -- Time when message was sent
    is_read BOOLEAN DEFAULT FALSE,                                    -- Check if read
    chat_id VARCHAR(255) NOT NULL,                                    -- Unique chat ID
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,  -- Refference check for sender ID
    FOREIGN KEY (reciever_id) REFERENCES users(id) ON DELETE CASCADE -- Refference check for reciever ID
);