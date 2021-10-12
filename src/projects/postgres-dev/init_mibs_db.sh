#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE mibs OWNER $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE mibs TO $POSTGRES_USER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "mibs" <<-EOSQL
    CREATE TABLE IF NOT EXISTS "Message" (
        "messageId" INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        "userId" TEXT NOT NULL,
        "message" TEXT NOT NULL,
        "sendTime" TIMESTAMP NOT NULL,
        "sent" BOOLEAN NOT NULL DEFAULT false,
        "lastSentTime" TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS "EmailMessageRecipient" (
        "messageSendRequestId" INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        "messageId" INTEGER NOT NULL,
        "email" TEXT NOT NULL,
        "sent" BOOLEAN NOT NULL DEFAULT false,
        "sendAttemptTime" TIMESTAMP,
        FOREIGN KEY ("messageId") REFERENCES "Message"("messageId")
    );
EOSQL