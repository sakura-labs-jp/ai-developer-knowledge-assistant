/* Idempotent Phase 0 users, positions, and Database/Cloud chains. */
SET XACT_ABORT ON;
BEGIN TRANSACTION;

MERGE dbo.KC_Position AS target
USING (VALUES
    (N'Database Engineer', N'Responsible for database performance, SQL, data processing and database operations.'),
    (N'Cloud Architect', N'Responsible for cloud infrastructure, architecture, networking, scalability and monitoring.'),
    (N'AI Engineer', N'Responsible for AI systems, RAG, LLM applications, embeddings and AI evaluation.')
) AS source (PositionName, Description)
ON target.PositionName = source.PositionName
WHEN MATCHED THEN UPDATE SET Description = source.Description
WHEN NOT MATCHED THEN INSERT (PositionName, Description)
VALUES (source.PositionName, source.Description);

MERGE dbo.KC_User AS target
USING (VALUES
    (N'Alice', N'alice@example.com'),
    (N'Bob', N'bob@example.com'),
    (N'Carol', N'carol@example.com')
) AS source (UserName, Email)
ON target.Email = source.Email
WHEN MATCHED THEN UPDATE SET UserName = source.UserName
WHEN NOT MATCHED THEN INSERT (UserName, Email)
VALUES (source.UserName, source.Email);

DECLARE @AliceId INT = (SELECT UserId FROM dbo.KC_User WHERE Email = N'alice@example.com');
DECLARE @BobId INT = (SELECT UserId FROM dbo.KC_User WHERE Email = N'bob@example.com');
DECLARE @CarolId INT = (SELECT UserId FROM dbo.KC_User WHERE Email = N'carol@example.com');
DECLARE @DbPositionId INT = (SELECT PositionId FROM dbo.KC_Position WHERE PositionName = N'Database Engineer');
DECLARE @CloudPositionId INT = (SELECT PositionId FROM dbo.KC_Position WHERE PositionName = N'Cloud Architect');
DECLARE @AiPositionId INT = (SELECT PositionId FROM dbo.KC_Position WHERE PositionName = N'AI Engineer');

INSERT INTO dbo.KC_UserPosition (UserId, PositionId)
SELECT data.UserId, data.PositionId
FROM (VALUES
    (@AliceId, @DbPositionId), (@AliceId, @CloudPositionId),
    (@BobId, @CloudPositionId), (@CarolId, @AiPositionId)
) data (UserId, PositionId)
WHERE NOT EXISTS
(
    SELECT 1 FROM dbo.KC_UserPosition existing
    WHERE existing.UserId = data.UserId AND existing.PositionId = data.PositionId
);

MERGE dbo.KC_KnowledgeSource AS target
USING (VALUES
    (N'Ticket', N'https://ticket.example.com/INC-001', N'Nightly Batch Processing Delay', N'OrderSystem', CAST(N'2026-08-10T09:00:00' AS DATETIME2)),
    (N'CSV', N'/operations/change_log_20260810.csv', N'Database Change Log', N'OrderSystem', CAST(N'2026-08-10T13:00:00' AS DATETIME2)),
    (N'PDF', N'/sharepoint/performance_report_20260810.pdf', N'Batch Performance Report', N'OrderSystem', CAST(N'2026-08-10T18:00:00' AS DATETIME2)),
    (N'Monitoring', N'/azure-monitor/vm_memory_metrics_20260810', N'Database VM Memory Investigation', N'OrderSystem', CAST(N'2026-08-10T12:00:00' AS DATETIME2)),
    (N'PDF', N'/sharepoint/cloud_resource_review_20260810.pdf', N'Cloud Resource Review Report', N'OrderSystem', CAST(N'2026-08-10T19:00:00' AS DATETIME2))
) AS source (SourceType, SourceLocation, Title, SystemName, SourceCreatedAt)
ON target.SourceLocation = source.SourceLocation
WHEN MATCHED THEN UPDATE SET
    SourceType = source.SourceType, Title = source.Title,
    SystemName = source.SystemName, SourceCreatedAt = source.SourceCreatedAt,
    UpdatedAt = SYSDATETIME()
WHEN NOT MATCHED THEN INSERT
    (SourceType, SourceLocation, Title, SystemName, SourceCreatedAt)
VALUES
    (source.SourceType, source.SourceLocation, source.Title, source.SystemName, source.SourceCreatedAt);

DECLARE @Incident NVARCHAR(MAX) = N'Nightly batch processing time increased from approximately 4 hours to 8 hours.';
DECLARE @DbResolution NVARCHAR(MAX) = N'SQL Server memory allocation was increased to reduce memory pressure during batch processing.';
DECLARE @DbResult NVARCHAR(MAX) = N'After increasing SQL Server memory allocation, batch processing time improved from 8 hours to approximately 4.5 hours.';
DECLARE @CloudResolution NVARCHAR(MAX) = N'Azure Monitor metrics were reviewed to investigate memory pressure on the database VM, and the VM memory capacity and resource sizing were evaluated.';
DECLARE @CloudResult NVARCHAR(MAX) = N'The infrastructure review confirmed sustained memory pressure on the database VM and identified resource sizing as an important factor affecting batch processing performance.';

INSERT INTO dbo.KC_Knowledge (SourceId, KnowledgeType, Content)
SELECT data.SourceId, data.KnowledgeType, data.Content
FROM
(
    SELECT SourceId, N'Incident' AS KnowledgeType, @Incident AS Content FROM dbo.KC_KnowledgeSource WHERE SourceLocation = N'https://ticket.example.com/INC-001'
    UNION ALL SELECT SourceId, N'Resolution', @DbResolution FROM dbo.KC_KnowledgeSource WHERE SourceLocation = N'/operations/change_log_20260810.csv'
    UNION ALL SELECT SourceId, N'Result', @DbResult FROM dbo.KC_KnowledgeSource WHERE SourceLocation = N'/sharepoint/performance_report_20260810.pdf'
    UNION ALL SELECT SourceId, N'Resolution', @CloudResolution FROM dbo.KC_KnowledgeSource WHERE SourceLocation = N'/azure-monitor/vm_memory_metrics_20260810'
    UNION ALL SELECT SourceId, N'Result', @CloudResult FROM dbo.KC_KnowledgeSource WHERE SourceLocation = N'/sharepoint/cloud_resource_review_20260810.pdf'
) data
WHERE NOT EXISTS
(
    SELECT 1 FROM dbo.KC_Knowledge existing
    WHERE existing.SourceId = data.SourceId
      AND existing.KnowledgeType = data.KnowledgeType
      AND existing.Content = data.Content
);

DECLARE @IncidentId INT = (SELECT KnowledgeId FROM dbo.KC_Knowledge WHERE Content = @Incident);
DECLARE @DbResolutionId INT = (SELECT KnowledgeId FROM dbo.KC_Knowledge WHERE Content = @DbResolution);
DECLARE @DbResultId INT = (SELECT KnowledgeId FROM dbo.KC_Knowledge WHERE Content = @DbResult);
DECLARE @CloudResolutionId INT = (SELECT KnowledgeId FROM dbo.KC_Knowledge WHERE Content = @CloudResolution);
DECLARE @CloudResultId INT = (SELECT KnowledgeId FROM dbo.KC_Knowledge WHERE Content = @CloudResult);

INSERT INTO dbo.KC_KnowledgePosition (KnowledgeId, PositionId)
SELECT data.KnowledgeId, data.PositionId
FROM (VALUES
    (@IncidentId, @DbPositionId), (@IncidentId, @CloudPositionId),
    (@DbResolutionId, @DbPositionId), (@DbResultId, @DbPositionId),
    (@DbResultId, @CloudPositionId), (@CloudResolutionId, @CloudPositionId),
    (@CloudResultId, @CloudPositionId)
) data (KnowledgeId, PositionId)
WHERE NOT EXISTS
(
    SELECT 1 FROM dbo.KC_KnowledgePosition existing
    WHERE existing.KnowledgeId = data.KnowledgeId
      AND existing.PositionId = data.PositionId
);

INSERT INTO dbo.KC_KnowledgeRelation
    (FromKnowledgeId, ToKnowledgeId, RelationType, Confidence)
SELECT data.FromId, data.ToId, data.RelationType, data.Confidence
FROM (VALUES
    (@IncidentId, @DbResolutionId, N'RESOLVED_BY', CAST(1.0000 AS DECIMAL(5,4))),
    (@DbResolutionId, @DbResultId, N'RESULTED_IN', CAST(1.0000 AS DECIMAL(5,4))),
    (@IncidentId, @CloudResolutionId, N'RESOLVED_BY', CAST(1.0000 AS DECIMAL(5,4))),
    (@CloudResolutionId, @CloudResultId, N'RESULTED_IN', CAST(1.0000 AS DECIMAL(5,4)))
) data (FromId, ToId, RelationType, Confidence)
WHERE NOT EXISTS
(
    SELECT 1 FROM dbo.KC_KnowledgeRelation existing
    WHERE existing.FromKnowledgeId = data.FromId
      AND existing.ToKnowledgeId = data.ToId
      AND existing.RelationType = data.RelationType
);

COMMIT TRANSACTION;
