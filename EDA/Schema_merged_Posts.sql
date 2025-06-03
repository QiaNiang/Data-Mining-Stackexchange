CREATE TABLE `Users` (
  `Id` INTEGER PRIMARY KEY,
  `Reputation` INTEGER NOT NULL,
  `CreationDate` DATETIME NOT NULL,
  `DisplayName` TEXT,
  `LastAccessDate` DATETIME NOT NULL,
  `WebsiteUrl` TEXT,
  `Location` TEXT,
  `AboutMe` TEXT,
  `Views` INTEGER NOT NULL,
  `UpVotes` INTEGER NOT NULL,
  `DownVotes` INTEGER NOT NULL,
  `ProfileImageUrl` TEXT,
  `EmailHash` TEXT,
  `AccountId` INTEGER
);

CREATE TABLE `Posts` (
  `Id` INTEGER PRIMARY KEY,
  `PostTypeId` INTEGER NOT NULL,
  `AcceptedAnswerId` INTEGER,
  `ParentId` INTEGER,
  `CreationDate` DATETIME NOT NULL,
  `DeletionDate` DATETIME,
  `Score` INTEGER NOT NULL,
  `ViewCount` INTEGER,
  `Body` TEXT,
  `OwnerUserId` INTEGER,
  `OwnerDisplayName` TEXT,
  `LastEditorUserId` INTEGER,
  `LastEditorDisplayName` TEXT,
  `LastEditDate` DATETIME,
  `LastActivityDate` DATETIME,
  `Title` TEXT,
  `Tags` TEXT,
  `AnswerCount` INTEGER,
  `CommentCount` INTEGER,
  `FavoriteCount` INTEGER,
  `ClosedDate` DATETIME,
  `CommunityOwnedDate` DATETIME
);

CREATE TABLE `Comments` (
  `Id` INTEGER PRIMARY KEY,
  `PostId` INTEGER NOT NULL,
  `Score` INTEGER NOT NULL,
  `Text` TEXT NOT NULL,
  `CreationDate` DATETIME NOT NULL,
  `UserDisplayName` TEXT,
  `UserId` INTEGER
);

CREATE TABLE `Votes` (
  `Id` INTEGER PRIMARY KEY,
  `PostId` INTEGER NOT NULL,
  `VoteTypeId` INTEGER NOT NULL,
  `UserId` INTEGER,
  `CreationDate` DATETIME,
  `BountyAmount` INTEGER
);

ALTER TABLE `Posts` ADD FOREIGN KEY (`OwnerUserId`) REFERENCES `Users` (`Id`);

ALTER TABLE `Posts` ADD FOREIGN KEY (`LastEditorUserId`) REFERENCES `Users` (`Id`);

ALTER TABLE `Posts` ADD FOREIGN KEY (`AcceptedAnswerId`) REFERENCES `Posts` (`Id`);

ALTER TABLE `Posts` ADD FOREIGN KEY (`ParentId`) REFERENCES `Posts` (`Id`);

ALTER TABLE `Comments` ADD FOREIGN KEY (`PostId`) REFERENCES `Posts` (`Id`);

ALTER TABLE `Comments` ADD FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`);

ALTER TABLE `Votes` ADD FOREIGN KEY (`PostId`) REFERENCES `Posts` (`Id`);

ALTER TABLE `Votes` ADD FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`);
