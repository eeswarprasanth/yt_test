from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
from dotenv import load_dotenv
from tools.custom_tool import youtube_transcript_extractor
from crewai_tools import TXTSearchTool

load_dotenv()


# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class YtTest():
	"""YtTest crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def transcript(self) -> Agent:
		return Agent(
			config=self.agents_config['transcript'],
			verbose=True,
			memory=True,
			tools=[youtube_transcript_extractor]
		)

	@agent
	def summarize(self) -> Agent:
		return Agent(
			config=self.agents_config['summarize'],
			verbose=True
		)
	

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def transcript_task(self) -> Task:
		return Task(
			config=self.tasks_config['transcript_task'],
			output_file='transcript.txt'

		)

	@task
	def summarize_task(self) -> Task:
		return Task(
			config=self.tasks_config['summarize_task'],
			output_file='summary.txt'
		)

	@agent
	def qa_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['qa_agent'],
			verbose=True,
			# tools=[tool]
		)

	@task
	def qa_task(self) -> Task:
		return Task(
			config=self.tasks_config['qa_task'],
			output_file='answer.txt',
			# tools=[tool]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the YtTest crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
