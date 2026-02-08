"""
Unit tests for TaskService.
"""
import pytest
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import Mock, patch
from src.services.task_service import TaskService
from src.models.task import TaskCreate, TaskUpdate


@pytest.fixture
def mock_session():
    """Mock database session for testing."""
    session = Mock(spec=Session)
    return session


def test_create_task_success(mock_session):
    """Test successful task creation."""
    # Arrange
    task_data = TaskCreate(user_id="test_user", title="Test task", description="Test description")

    # Mock the task object that will be added
    from src.models.task import Task
    mock_task = Task(id=1, **task_data.model_dump())

    # Configure the session mock
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock(return_value=mock_task)

    # Act
    result = TaskService.create_task(mock_session, task_data)

    # Assert
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert result.title == "Test task"
    assert result.description == "Test description"
    assert result.user_id == "test_user"


def test_get_task_by_id_success(mock_session):
    """Test successful retrieval of a task by ID."""
    # Arrange
    from src.models.task import Task
    expected_task = Task(id=1, user_id="test_user", title="Test task", completed=False)
    mock_session.get.return_value = expected_task

    # Act
    result = TaskService.get_task_by_id(mock_session, 1, "test_user")

    # Assert
    mock_session.get.assert_called_once_with(Task, 1)
    assert result == expected_task


def test_get_task_by_id_wrong_user(mock_session):
    """Test retrieval of a task by ID for wrong user."""
    # Arrange
    from src.models.task import Task
    task = Task(id=1, user_id="other_user", title="Test task", completed=False)
    mock_session.get.return_value = task

    # Act
    result = TaskService.get_task_by_id(mock_session, 1, "test_user")

    # Assert
    assert result is None


def test_get_tasks_by_user(mock_session):
    """Test retrieval of tasks by user."""
    # Arrange
    from src.models.task import Task
    from sqlmodel import select
    from sqlalchemy import Row
    from unittest.mock import MagicMock

    # Create mock tasks
    task1 = Task(id=1, user_id="test_user", title="Task 1", completed=False)
    task2 = Task(id=2, user_id="test_user", title="Task 2", completed=True)

    # Create a mock result that behaves like a SQL execution result
    mock_exec_result = MagicMock()
    mock_exec_result.all.return_value = [task1, task2]

    # Mock the exec method to return our mock result
    mock_session.exec.return_value = mock_exec_result

    # Act
    result = TaskService.get_tasks_by_user(mock_session, "test_user")

    # Assert
    mock_session.exec.assert_called()  # Called with a select query
    assert len(result) == 2
    assert result[0].title == "Task 1"
    assert result[1].title == "Task 2"


def test_update_task_success(mock_session):
    """Test successful task update."""
    # Arrange
    from src.models.task import Task
    existing_task = Task(id=1, user_id="test_user", title="Old title", completed=False)
    mock_session.get.return_value = existing_task

    update_data = TaskUpdate(title="New title", completed=True)

    # Act
    result = TaskService.update_task(mock_session, 1, "test_user", update_data)

    # Assert
    mock_session.get.assert_called_once_with(Task, 1)
    mock_session.add.assert_called_once_with(existing_task)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert result.title == "New title"
    assert result.completed is True


def test_complete_task_success(mock_session):
    """Test successful task completion."""
    # Arrange
    from src.models.task import Task
    existing_task = Task(id=1, user_id="test_user", title="Test task", completed=False)
    mock_session.get.return_value = existing_task

    # Act
    result = TaskService.complete_task(mock_session, 1, "test_user")

    # Assert
    mock_session.get.assert_called_once_with(Task, 1)
    mock_session.add.assert_called_once_with(existing_task)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert result.completed is True


def test_delete_task_success(mock_session):
    """Test successful task deletion."""
    # Arrange
    from src.models.task import Task
    existing_task = Task(id=1, user_id="test_user", title="Test task", completed=False)
    mock_session.get.return_value = existing_task
    mock_session.delete = Mock()
    mock_session.commit = Mock()

    # Act
    result = TaskService.delete_task(mock_session, 1, "test_user")

    # Assert
    mock_session.get.assert_called_once_with(Task, 1)
    mock_session.delete.assert_called_once_with(existing_task)
    mock_session.commit.assert_called_once()
    assert result is True


def test_delete_task_wrong_user(mock_session):
    """Test deletion of a task by wrong user."""
    # Arrange
    from src.models.task import Task
    task = Task(id=1, user_id="other_user", title="Test task", completed=False)
    mock_session.get.return_value = task

    # Act
    result = TaskService.delete_task(mock_session, 1, "test_user")

    # Assert
    assert result is False