import os
import json
import click

from pman.utils import is_valid_name

ENV_PREFIX = 'PMAN_'
DEFAULT_PMAN_DIR = '.pmanprojects'


@click.group()
@click.pass_context
@click.option('--path', help='Pman projects path', envvar='PROJETS_PATH',
	default=lambda: os.path.join(os.path.expanduser('~'), DEFAULT_PMAN_DIR))
def cli(ctx, path):
	"""
	Simple project manager for terminal

	Example:
		pman new project_name [Create new project called project_name]
			--path - Project path
		pman project_name [Switch to project called project_name]
		pman edit project_name [Edit a project]
		pman rename project_name new_project_name
		pman list [List of pprojects]
	"""
	ctx.obj = {
		'path': path
	}


@cli.command()
@click.pass_context
@click.argument('project_name')
@click.option('--path', prompt='Project path (current path as default if empty)',
	default=lambda: os.getcwd())
def new(ctx, project_name, path):
	# Validate username
	if not is_valid_name(project_name):
		error_text = ("\n Invalid project name. \n"
		"\t - Special character are not allowed except - and _. \n"
		"\t - Only lowercase charactera and numbers are allowed \n")
		click.echo(click.style(error_text, fg='red'))
		return

	project_path = os.path.join(ctx.obj['path'], project_name)

	# Check if project exists
	if os.path.exists(project_path):
		error_text = 'Project \"{}\" already exists'.format(project_name)
		click.echo(click.style(error_text, fg='red'))
		return

	# create project
	os.makedirs(project_path)

	project_path_file = os.path.join(project_path, 'path')
	with click.open_file(project_path_file, 'w') as f:
		f.write(path)

	initial_commands = [
		{
			'name': 'Sample command',
			'commands': [
				'echo Hello world!!'
			],
			'run_default': True
		}
	]

	commands_file = os.path.join(project_path, 'commands.json')
	with click.open_file(commands_file, 'w') as f:
		f.write(json.dumps(initial_commands, sort_keys=True, indent=4))

	success_text = 'New project {} created at {}'.format(project_name, project_path)
	click.echo(click.style(success_text, fg='green'))


@cli.command()
@click.pass_context
@click.argument('project_name')
def switch(ctx, project_name):
	project_path = os.path.join(ctx.obj['path'], project_name)

	# Check if project exists
	if not os.path.exists(project_path):
		error_text = 'Project \"{}\" doest\'t exist.'.format(project_name)
		click.echo(click.style(error_text, fg='red'))
		return

	try:
		project_path_file = os.path.join(project_path, 'path')
		with click.open_file(project_path_file, 'r') as f:
			target_project_path = f.read()
	except:
		click.echo(click.style('Corrupt project : {}'.format(project_name), fg='red'))

	print(target_project_path)
	try:
		os.chdir(target_project_path)
		# os.system("/bin/zsh")
	except:
		click.echo(click.style('Couldn\'t change path to : {}'.format(target_project_path), fg='red'))

	click.echo(click.style('Switched to project : {}'.format(project_name), fg='green'))


@cli.command()
@click.pass_context
def list(ctx):
	projects_path = ctx.obj['path']

	projects = []
	for (dirpath, dirnames, filenames) in os.walk(projects_path):
		projects = dirnames
		break

	for project in projects:
		click.echo(click.style(project, fg='green'))


@cli.command()
def rename():
	click.echo('Rename project')


@cli.command()
def edit():
	click.echo('Edit project')
