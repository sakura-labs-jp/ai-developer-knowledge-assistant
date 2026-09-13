/* Phase 1: expand the supported Knowledge Chain node types. */
SET XACT_ABORT ON;
BEGIN TRANSACTION;

IF EXISTS
(
    SELECT 1
    FROM sys.check_constraints
    WHERE name = N'CK_KC_Knowledge_Type'
      AND parent_object_id = OBJECT_ID(N'dbo.KC_Knowledge')
)
BEGIN
    ALTER TABLE dbo.KC_Knowledge
        DROP CONSTRAINT CK_KC_Knowledge_Type;
END;

ALTER TABLE dbo.KC_Knowledge WITH CHECK
ADD CONSTRAINT CK_KC_Knowledge_Type
CHECK
(
    KnowledgeType IN
    (
        N'Incident',
        N'Analysis',
        N'Resolution',
        N'Decision',
        N'Result'
    )
);

ALTER TABLE dbo.KC_Knowledge
    CHECK CONSTRAINT CK_KC_Knowledge_Type;

COMMIT TRANSACTION;
