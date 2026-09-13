/* Current Knowledge Chain schema for a new SQL Server environment. */

CREATE TABLE dbo.KC_User
(
    UserId INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_KC_User PRIMARY KEY,
    UserName NVARCHAR(200) NOT NULL,
    Email NVARCHAR(300) NULL,
    CreatedAt DATETIME2(7) NOT NULL CONSTRAINT DF_KC_User_CreatedAt DEFAULT SYSDATETIME(),
    CONSTRAINT UQ_KC_User_Email UNIQUE (Email)
);

CREATE TABLE dbo.KC_Position
(
    PositionId INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_KC_Position PRIMARY KEY,
    PositionName NVARCHAR(200) NOT NULL,
    Description NVARCHAR(1000) NULL,
    CreatedAt DATETIME2(7) NOT NULL CONSTRAINT DF_KC_Position_CreatedAt DEFAULT SYSDATETIME(),
    CONSTRAINT UQ_KC_Position_Name UNIQUE (PositionName)
);

CREATE TABLE dbo.KC_UserPosition
(
    UserId INT NOT NULL,
    PositionId INT NOT NULL,
    CreatedAt DATETIME2(7) NOT NULL CONSTRAINT DF_KC_UserPosition_CreatedAt DEFAULT SYSDATETIME(),
    CONSTRAINT PK_KC_UserPosition PRIMARY KEY (UserId, PositionId),
    CONSTRAINT FK_KC_UserPosition_User FOREIGN KEY (UserId) REFERENCES dbo.KC_User(UserId),
    CONSTRAINT FK_KC_UserPosition_Position FOREIGN KEY (PositionId) REFERENCES dbo.KC_Position(PositionId)
);

CREATE TABLE dbo.KC_KnowledgeSource
(
    SourceId INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_KC_KnowledgeSource PRIMARY KEY,
    SourceType NVARCHAR(50) NOT NULL,
    SourceLocation NVARCHAR(2000) NOT NULL,
    Title NVARCHAR(500) NULL,
    SystemName NVARCHAR(200) NULL,
    SourceCreatedAt DATETIME2(7) NULL,
    CreatedAt DATETIME2(7) NOT NULL CONSTRAINT DF_KC_KnowledgeSource_CreatedAt DEFAULT SYSDATETIME(),
    UpdatedAt DATETIME2(7) NOT NULL CONSTRAINT DF_KC_KnowledgeSource_UpdatedAt DEFAULT SYSDATETIME()
);

CREATE TABLE dbo.KC_Knowledge
(
    KnowledgeId INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_KC_Knowledge PRIMARY KEY,
    SourceId INT NOT NULL,
    KnowledgeType NVARCHAR(50) NOT NULL,
    Content NVARCHAR(MAX) NOT NULL,
    CreatedAt DATETIME2(7) NOT NULL CONSTRAINT DF_KC_Knowledge_CreatedAt DEFAULT SYSDATETIME(),
    UpdatedAt DATETIME2(7) NOT NULL CONSTRAINT DF_KC_Knowledge_UpdatedAt DEFAULT SYSDATETIME(),
    CONSTRAINT FK_KC_Knowledge_Source FOREIGN KEY (SourceId) REFERENCES dbo.KC_KnowledgeSource(SourceId),
    CONSTRAINT CK_KC_Knowledge_Type CHECK
    (
        KnowledgeType IN (N'Incident', N'Analysis', N'Resolution', N'Decision', N'Result')
    )
);

CREATE TABLE dbo.KC_KnowledgePosition
(
    KnowledgeId INT NOT NULL,
    PositionId INT NOT NULL,
    CreatedAt DATETIME2(7) NOT NULL CONSTRAINT DF_KC_KnowledgePosition_CreatedAt DEFAULT SYSDATETIME(),
    CONSTRAINT PK_KC_KnowledgePosition PRIMARY KEY (KnowledgeId, PositionId),
    CONSTRAINT FK_KC_KnowledgePosition_Knowledge FOREIGN KEY (KnowledgeId) REFERENCES dbo.KC_Knowledge(KnowledgeId),
    CONSTRAINT FK_KC_KnowledgePosition_Position FOREIGN KEY (PositionId) REFERENCES dbo.KC_Position(PositionId)
);

CREATE TABLE dbo.KC_KnowledgeRelation
(
    RelationId INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_KC_KnowledgeRelation PRIMARY KEY,
    FromKnowledgeId INT NOT NULL,
    ToKnowledgeId INT NOT NULL,
    RelationType NVARCHAR(100) NOT NULL,
    Confidence DECIMAL(5,4) NULL,
    CreatedAt DATETIME2(7) NOT NULL CONSTRAINT DF_KC_KnowledgeRelation_CreatedAt DEFAULT SYSDATETIME(),
    CONSTRAINT FK_KC_KnowledgeRelation_From FOREIGN KEY (FromKnowledgeId) REFERENCES dbo.KC_Knowledge(KnowledgeId),
    CONSTRAINT FK_KC_KnowledgeRelation_To FOREIGN KEY (ToKnowledgeId) REFERENCES dbo.KC_Knowledge(KnowledgeId),
    CONSTRAINT CK_KC_KnowledgeRelation_Self CHECK (FromKnowledgeId <> ToKnowledgeId),
    CONSTRAINT CK_KC_KnowledgeRelation_Confidence CHECK
        (Confidence IS NULL OR Confidence BETWEEN 0 AND 1),
    CONSTRAINT UQ_KC_KnowledgeRelation UNIQUE
        (FromKnowledgeId, ToKnowledgeId, RelationType)
);

CREATE TABLE dbo.KC_KnowledgeEmbedding
(
    EmbeddingId INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_KC_KnowledgeEmbedding PRIMARY KEY,
    KnowledgeId INT NOT NULL,
    EmbeddingModel NVARCHAR(100) NOT NULL,
    EmbeddingVector NVARCHAR(MAX) NOT NULL,
    CreatedAt DATETIME2(7) NOT NULL CONSTRAINT DF_KC_KnowledgeEmbedding_CreatedAt DEFAULT SYSDATETIME(),
    CONSTRAINT FK_KC_KnowledgeEmbedding_Knowledge FOREIGN KEY (KnowledgeId) REFERENCES dbo.KC_Knowledge(KnowledgeId),
    CONSTRAINT UQ_KC_KnowledgeEmbedding UNIQUE (KnowledgeId, EmbeddingModel)
);
