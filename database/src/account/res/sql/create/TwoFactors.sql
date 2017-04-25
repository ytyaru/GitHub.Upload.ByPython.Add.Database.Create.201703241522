create table TwoFactors(
    Id          integer primary key,
    AccountId   integer not null,
    Secret      text not null,
    foreign key(AccountId) references Accounts(Id)
);
