create table AccessTokens(
    Id              integer primary key,
    AccountId       integer not null,
    IdOnGitHub      integer unique not null,
    Note            text,
    AccessToken     text not null,
    Scopes          text,
    foreign key(AccountId) references Accounts(Id)
);
