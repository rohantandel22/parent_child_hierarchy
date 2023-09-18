/*#######################################################################################################################
# Developer    : Rohan Tandel
# Description  : Find Ultimate Parent Loan ID for given Loan_id and Parent_Loan_id data built in temporary table
#######################################################################################################################*/

CREATE OR REPLACE TEMPORARY TABLE tt_loan_rel
(
 loan_id INT64,
 parent_loan_id INT64
);

INSERT INTO tt_loan_rel
VALUES 
(100,600),
(200,NULL),
(600,200),
(300,NULL)
/*
We can add this test the recursion for more levels
,
(400,600),
(500,400),
(700,500),
(800,300),
(900,800),
(1000,900),
(1001,900),
(1002,1001),
(1003,1002),
(1004,1003),
(1005,1004)*/
;

WITH RECURSIVE parent_child_rel
AS
(
  SELECT loan_id, 
         parent_loan_id, 
         loan_id AS ultimate_parent_loan_id
    FROM tt_loan_rel 
   WHERE parent_loan_id IS NULL
   UNION ALL
  SELECT t.loan_id, 
         t.parent_loan_id, 
         ultimate_parent_loan_id
    FROM parent_child_rel AS p 
    JOIN tt_loan_rel AS t 
      ON t.parent_loan_id = p.loan_id
)
SELECT *
  FROM parent_child_rel p
 ORDER BY 3,1;

