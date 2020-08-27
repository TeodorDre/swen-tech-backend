create schema if not exists swentech;
drop schema swentech cascade;
create schema if not exists swentech;

CREATE TABLE if not exists swentech.users (
  client_id     SERIAL      PRIMARY KEY NOT NULL unique,
  client_name   TEXT        NOT NULL,
  client_email  TEXT        NOT NULL unique,

  password      TEXT        NOT NULL,

  created_ts    TIMESTAMPTZ NOT NULL default now(),
  updated_ts    TIMESTAMPTZ NOT NULL default now()
);

CREATE TABLE if not exists swentech.sessions (
  client_id     SERIAL      not null unique references swentech.users ON DELETE CASCADE,
  session_id    TEXT        NOT NULL unique,

  created_ts    TIMESTAMPTZ NOT NULL default now(),
  CONSTRAINT CL_SESS UNIQUE (client_id, session_id)
);

CREATE TABLE if not exists swentech.categories (
  client_id     SERIAL      not null unique references swentech.users ON DELETE CASCADE,
  session_id    TEXT        NOT NULL unique,

  created_ts    TIMESTAMPTZ NOT NULL default now(),
  CONSTRAINT CL_SESS UNIQUE (client_id, session_id)
);

CREATE TABLE if not exists swentech.categories_lang (
  client_id     SERIAL      not null unique references swentech.users ON DELETE CASCADE,
  session_id    TEXT        NOT NULL unique,

  created_ts    TIMESTAMPTZ NOT NULL default now(),
  CONSTRAINT CL_SESS UNIQUE (client_id, session_id)
);

CREATE TABLE if not exists swentech.tags (
  client_id     SERIAL      not null unique references swentech.users ON DELETE CASCADE,
  session_id    TEXT        NOT NULL unique,

  created_ts    TIMESTAMPTZ NOT NULL default now(),
  CONSTRAINT CL_SESS UNIQUE (client_id, session_id)
);

CREATE TABLE if not exists swentech.tags_lang (
  client_id     SERIAL      not null unique references swentech.users ON DELETE CASCADE,
  session_id    TEXT        NOT NULL unique,

  created_ts    TIMESTAMPTZ NOT NULL default now(),
  CONSTRAINT CL_SESS UNIQUE (client_id, session_id)
);

CREATE TABLE if not exists swentech.posts (
  client_id     SERIAL      not null unique references swentech.users ON DELETE CASCADE,
  session_id    TEXT        NOT NULL unique,

  created_ts    TIMESTAMPTZ NOT NULL default now(),
  CONSTRAINT CL_SESS UNIQUE (client_id, session_id)
);

CREATE TABLE if not exists swentech.posts_lang (
  client_id     SERIAL      not null unique references swentech.users ON DELETE CASCADE,
  session_id    TEXT        NOT NULL unique,

  created_ts    TIMESTAMPTZ NOT NULL default now(),
  CONSTRAINT CL_SESS UNIQUE (client_id, session_id)
);