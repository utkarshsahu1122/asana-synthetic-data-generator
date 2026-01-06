-- Core entity counts
SELECT 'organizations' AS entity, COUNT(*) FROM organizations;
SELECT 'teams' AS entity, COUNT(*) FROM teams;
SELECT 'users' AS entity, COUNT(*) FROM users;
SELECT 'projects' AS entity, COUNT(*) FROM projects;
SELECT 'sections' AS entity, COUNT(*) FROM sections;
SELECT 'tasks' AS entity, COUNT(*) FROM tasks;
SELECT 'comments' AS entity, COUNT(*) FROM comments;

-- Tasks with invalid project references (should be 0)
SELECT COUNT(*) AS orphan_tasks
FROM tasks
WHERE project_id NOT IN (SELECT project_id FROM projects);

-- Tasks with invalid assignees (should be 0)
SELECT COUNT(*) AS invalid_assignees
FROM tasks
WHERE assignee_id IS NOT NULL
  AND assignee_id NOT IN (SELECT user_id FROM users);

-- Tasks completed before they were created (should be 0)
SELECT COUNT(*) AS invalid_completion_times
FROM tasks
WHERE completed = 1
  AND completed_at < created_at;

-- Tasks updated before creation (should be 0)
SELECT COUNT(*) AS invalid_updates
FROM tasks
WHERE updated_at < created_at;

-- Completion rate
SELECT
  ROUND(100.0 * SUM(completed) / COUNT(*), 2) AS completion_percentage
FROM tasks;

-- Completion by project type
SELECT
  p.project_type,
  COUNT(*) AS total_tasks,
  SUM(t.completed) AS completed_tasks
FROM tasks t
JOIN projects p ON t.project_id = p.project_id
GROUP BY p.project_type;

-- Number of subtasks
SELECT COUNT(*) AS subtask_count
FROM tasks
WHERE parent_task_id IS NOT NULL;

-- Subtasks without valid parents (should be 0)
SELECT COUNT(*) AS orphan_subtasks
FROM tasks
WHERE parent_task_id IS NOT NULL
  AND parent_task_id NOT IN (SELECT task_id FROM tasks);

-- Tasks with comments
SELECT
  COUNT(DISTINCT task_id) AS tasks_with_comments,
  (SELECT COUNT(*) FROM tasks) AS total_tasks
FROM comments;

-- Average comments per completed task
SELECT
  ROUND(AVG(comment_count), 2) AS avg_comments_per_completed_task
FROM (
  SELECT t.task_id, COUNT(c.comment_id) AS comment_count
  FROM tasks t
  LEFT JOIN comments c ON t.task_id = c.task_id
  WHERE t.completed = 1
  GROUP BY t.task_id
);

-- Tasks should increase on every run
SELECT COUNT(*) FROM tasks;

-- Core entities should remain stable
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM projects;
