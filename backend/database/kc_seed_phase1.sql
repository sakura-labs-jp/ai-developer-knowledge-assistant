/* Phase 1: add an AI Engineer chain to the existing batch incident. */
SET XACT_ABORT ON;
BEGIN TRANSACTION;

DECLARE @AiPositionId INT =
(
    SELECT PositionId FROM dbo.KC_Position
    WHERE PositionName = N'AI Engineer'
);
DECLARE @IncidentId INT =
(
    SELECT KnowledgeId FROM dbo.KC_Knowledge
    WHERE Content = N'Nightly batch processing time increased from approximately 4 hours to 8 hours.'
);

IF @AiPositionId IS NULL
    THROW 50001, 'AI Engineer position was not found.', 1;
IF @IncidentId IS NULL
    THROW 50002, 'Phase 0 incident was not found.', 1;

MERGE dbo.KC_KnowledgeSource AS target
USING (VALUES
    (N'Monitoring', N'/ai-monitoring/batch_anomaly_analysis_20260810.json',
     N'AI-assisted Batch Anomaly Analysis', N'OrderSystem',
     CAST(N'2026-08-10T18:30:00' AS DATETIME2)),
    (N'ADR', N'/architecture/ADR-017-grounded-incident-analysis.md',
     N'Grounded Incident Analysis Design', N'KnowledgeAssistant',
     CAST(N'2026-08-11T09:00:00' AS DATETIME2))
) AS source (SourceType, SourceLocation, Title, SystemName, SourceCreatedAt)
ON target.SourceLocation = source.SourceLocation
WHEN MATCHED THEN UPDATE SET
    SourceType = source.SourceType,
    Title = source.Title,
    SystemName = source.SystemName,
    SourceCreatedAt = source.SourceCreatedAt,
    UpdatedAt = SYSDATETIME()
WHEN NOT MATCHED THEN INSERT
    (SourceType, SourceLocation, Title, SystemName, SourceCreatedAt)
VALUES
    (source.SourceType, source.SourceLocation, source.Title,
     source.SystemName, source.SourceCreatedAt);

DECLARE @AnalysisContent NVARCHAR(MAX) =
    N'AI-assisted analysis correlated the batch execution window with the sustained database VM memory-pressure period recorded in monitoring data.';
DECLARE @DecisionContent NVARCHAR(MAX) =
    N'The incident assistant was designed to retrieve ticket, monitoring, change-log, and performance-report evidence while keeping confirmed facts separate from inferred causes.';

INSERT INTO dbo.KC_Knowledge (SourceId, KnowledgeType, Content)
SELECT data.SourceId, data.KnowledgeType, data.Content
FROM
(
    SELECT SourceId, N'Analysis' AS KnowledgeType, @AnalysisContent AS Content
    FROM dbo.KC_KnowledgeSource
    WHERE SourceLocation = N'/ai-monitoring/batch_anomaly_analysis_20260810.json'
    UNION ALL
    SELECT SourceId, N'Decision', @DecisionContent
    FROM dbo.KC_KnowledgeSource
    WHERE SourceLocation = N'/architecture/ADR-017-grounded-incident-analysis.md'
) data
WHERE NOT EXISTS
(
    SELECT 1 FROM dbo.KC_Knowledge existing
    WHERE existing.SourceId = data.SourceId
      AND existing.KnowledgeType = data.KnowledgeType
      AND existing.Content = data.Content
);

DECLARE @AnalysisId INT =
    (SELECT KnowledgeId FROM dbo.KC_Knowledge WHERE Content = @AnalysisContent);
DECLARE @DecisionId INT =
    (SELECT KnowledgeId FROM dbo.KC_Knowledge WHERE Content = @DecisionContent);

INSERT INTO dbo.KC_KnowledgePosition (KnowledgeId, PositionId)
SELECT data.KnowledgeId, @AiPositionId
FROM (VALUES (@AnalysisId), (@DecisionId)) data (KnowledgeId)
WHERE NOT EXISTS
(
    SELECT 1 FROM dbo.KC_KnowledgePosition existing
    WHERE existing.KnowledgeId = data.KnowledgeId
      AND existing.PositionId = @AiPositionId
);

INSERT INTO dbo.KC_KnowledgeRelation
    (FromKnowledgeId, ToKnowledgeId, RelationType, Confidence)
SELECT data.FromId, data.ToId, data.RelationType, data.Confidence
FROM (VALUES
    (@IncidentId, @AnalysisId, N'ANALYZED_BY', CAST(0.9500 AS DECIMAL(5,4))),
    (@AnalysisId, @DecisionId, N'INFORMED', CAST(0.9500 AS DECIMAL(5,4)))
) data (FromId, ToId, RelationType, Confidence)
WHERE NOT EXISTS
(
    SELECT 1 FROM dbo.KC_KnowledgeRelation existing
    WHERE existing.FromKnowledgeId = data.FromId
      AND existing.ToKnowledgeId = data.ToId
      AND existing.RelationType = data.RelationType
);

COMMIT TRANSACTION;
