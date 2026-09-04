SELECT format('CREATE ROLE %I LOGIN', :'chat_db_user')
WHERE NOT EXISTS (
  SELECT FROM pg_catalog.pg_roles WHERE rolname = :'chat_db_user'
) \gexec

SELECT format(
  'ALTER ROLE %I WITH LOGIN PASSWORD %L',
  :'chat_db_user',
  :'chat_db_password'
) \gexec

SELECT format('CREATE DATABASE %I OWNER %I', :'chat_db_name', :'chat_db_user')
WHERE NOT EXISTS (
  SELECT FROM pg_catalog.pg_database WHERE datname = :'chat_db_name'
) \gexec

SELECT format('ALTER DATABASE %I OWNER TO %I', :'chat_db_name', :'chat_db_user') \gexec
