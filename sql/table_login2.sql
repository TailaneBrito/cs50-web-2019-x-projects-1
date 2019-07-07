CREATE EXTENSION chkpass;
CREATE EXTENSION pgcrypto;
CREATE TABLE login2(
      usr_id SERIAL PRIMARY KEY,
      usr_name VARCHAR UNIQUE NOT NULL,
      usr_pass TEXT NOT NULL 
 );
