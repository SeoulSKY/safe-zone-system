/* This file creates all the postgres database tables */

create table if not exists Message (
    messageId serial primary key,
    userId text not null,
    message text not null,
    sendTime timestamp not null,
    sent boolean not null default false,
    lastSentTime timestamp
);

create table if not exists EmailMessageRecipient (
    messageSendRequestId serial primary key,
    messageId int not null,
    email text not null,
    sent boolean not null default false,
    sendAttemptTime timestamp,
    foreign key (messageId) references Message(messageId)
);
