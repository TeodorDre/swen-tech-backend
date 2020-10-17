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

  CONSTRAINT    CL_SESS     UNIQUE (session_id, client_id)
);

CREATE TABLE if not exists swentech.categories (
  client_id       SERIAL               not null references swentech.users,

  category_id     SERIAL               PRIMARY KEY not null unique,
  category_slug   TEXT                 NOT NULL unique,

  created_ts      TIMESTAMPTZ          NOT NULL default now(),
  updated_ts      TIMESTAMPTZ          NOT NULL default now(),

  CONSTRAINT      CL_CATEGORY_CREATED  UNIQUE (category_id, client_id)
);

CREATE TABLE if not exists swentech.categories_lang (
  category_id      SERIAL      not null unique references swentech.categories ON DELETE CASCADE,

  category_lang_id SERIAL      PRIMARY KEY NOT NULL unique,

  name_ru          TEXT        NOT NULL,
  name_en          TEXT        NOT NULL,
  name_fr          TEXT        NOT NULL,

  created_ts       TIMESTAMPTZ NOT NULL default now(),
  updated_ts       TIMESTAMPTZ NOT NULL default now(),

  CONSTRAINT       CL_CATEGORY UNIQUE (category_lang_id, category_id)
);

CREATE TABLE if not exists swentech.tags (
  client_id       SERIAL          NOT NULL REFERENCES swentech.users,

  tag_id          SERIAL          PRIMARY KEY not null unique,
  tag_slug        TEXT            NOT NULL unique,

  created_ts      TIMESTAMPTZ     NOT NULL default now(),
  updated_ts      TIMESTAMPTZ     NOT NULL default now(),

  CONSTRAINT      CL_TAG_CREATED  UNIQUE (tag_id, client_id)
);

CREATE TABLE if not exists swentech.tags_lang (
  tag_id          SERIAL      not null unique references swentech.tags ON DELETE CASCADE,

  tag_lang_id     SERIAL      PRIMARY KEY NOT NULL unique,

  name_ru         TEXT        NOT NULL,
  name_en         TEXT        NOT NULL,
  name_fr         TEXT        NOT NULL,

  created_ts      TIMESTAMPTZ NOT NULL default now(),
  updated_ts      TIMESTAMPTZ NOT NULL default now(),

  CONSTRAINT      CL_TAG      UNIQUE (tag_lang_id, tag_id)
);

CREATE TABLE if not exists swentech.posts (
  client_id               SERIAL           NOT NULL REFERENCES swentech.users,
  category_id             SERIAL           NOT NULL REFERENCES swentech.categories,

  post_id                 SERIAL           PRIMARY KEY not null unique,
  post_slug               TEXT             NOT NULL unique,
  post_url                TEXT             NOT NULL unique,

  post_featured_image     TEXT             NOT NULL unique,
  post_status             SERIAL           NOT NULL unique,
  post_tags_id            NUMERIC[]        NOT NULL unique,

  created_ts              TIMESTAMPTZ      NOT NULL default now(),
  updated_ts              TIMESTAMPTZ      NOT NULL default now()
);

CREATE TABLE if not exists swentech.posts_lang (
  post_id          SERIAL      NOT NULL UNIQUE REFERENCES  swentech.posts ON DELETE CASCADE,

  post_lang_id     SERIAL      PRIMARY KEY NOT NULL unique,

  title_ru         TEXT        NOT NULL,
  title_en         TEXT        NOT NULL,
  title_fr         TEXT        NOT NULL,

  text_ru          TEXT        NOT NULL,
  text_en          TEXT        NOT NULL,
  text_fr          TEXT        NOT NULL,

  created_ts      TIMESTAMPTZ  NOT NULL default now(),
  updated_ts      TIMESTAMPTZ  NOT NULL default now(),

  CONSTRAINT POST_ID UNIQUE (post_lang_id, post_id)
);