create schema if not exists markup;
drop schema markup cascade;
create schema if not exists markup;

CREATE TABLE if not exists markup.users (
  client_id     SERIAL      PRIMARY KEY NOT NULL unique,
  client_name   TEXT        NOT NULL,
  client_email  TEXT        NOT NULL unique,

  password      TEXT        NOT NULL,

  created_ts    TIMESTAMPTZ NOT NULL default now(),
  updated_ts    TIMESTAMPTZ NOT NULL default now()
);

CREATE TABLE if not exists markup.sessions (
  client_id     SERIAL      not null unique references markup.users ON DELETE CASCADE,
  session_id    TEXT        NOT NULL unique,

  created_ts    TIMESTAMPTZ NOT NULL default now(),
  CONSTRAINT CL_SESS UNIQUE (client_id, session_id)
);

CREATE TABLE if not exists markup.projects (
  project_id          SERIAL PRIMARY KEY,
  project_name        TEXT        NOT NULL unique,
  project_description TEXT,
  created_ts          TIMESTAMPTZ NOT NULL default now(),
  updated_ts          TIMESTAMPTZ NOT NULL default now()
);

CREATE TABLE if not exists markup.datasets (
  dataset_id          SERIAL PRIMARY KEY,
  dataset_name        TEXT        NOT NULL,
  dataset_description TEXT,
  project_id          bigint      not null references markup.projects ON DELETE CASCADE,
  created_ts          TIMESTAMPTZ NOT NULL default now(),
  updated_ts          TIMESTAMPTZ NOT NULL default now(),
  CONSTRAINT DS_PROJ UNIQUE (dataset_name, project_id)
);

CREATE TABLE if not exists markup.images (
  image_id          BIGSERIAL PRIMARY KEY,
  image_name        TEXT        NOT NULL,
  image_description TEXT,
  image_link        TEXT        not null,
  width             INTEGER     NOT NULL,
  height            INTEGER     NOT NULL,
  dataset_id        BIGINT      not null references markup.datasets ON DELETE CASCADE,
  created_ts        TIMESTAMPTZ NOT NULL default now(),
  updated_ts        TIMESTAMPTZ NOT NULL default now(),
  CONSTRAINT IM_DS UNIQUE (image_name, dataset_id),
  CONSTRAINT LINK_DS UNIQUE (image_link, dataset_id)
);

CREATE TABLE if not exists markup.labels (
  label_id          SERIAL PRIMARY KEY,
  label_name        TEXT        NOT NULL unique,
  label_description TEXT,
  color             TEXT        not null,
  parameters        JSONB,
  created_ts        TIMESTAMPTZ NOT NULL default now(),
  updated_ts        TIMESTAMPTZ NOT NULL default now()
);

CREATE TABLE if not exists markup.annotations (
  image_id    BIGINT      not null unique references markup.images ON DELETE CASCADE,
  annotations JSONB       not null,
  created_ts  TIMESTAMPTZ NOT NULL default now(),
  updated_ts  TIMESTAMPTZ NOT NULL default now()
);