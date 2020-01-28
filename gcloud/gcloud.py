import json
import subprocess
import errno
import os

from system.system import System

class GCloud:

    @staticmethod
    def is_installed():
        try:
            with open(os.devnull, 'wb') as devnull:
                subprocess.check_call(['gcloud', '-v'], stdout=devnull, stderr=subprocess.STDOUT)
            return True
        except OSError as e:
            if e.errno == errno.ENOENT:
                return False
            else:
                # Something else went wrong while trying to run `wget`
                raise

    @staticmethod
    def copy_file_from_remote(remote_file_location, local_target):
        try:
            System.run_command('gcloud compute scp {}:~/{} {}'.format(INSTANCE_NAME, remote_file_location, local_target))
            return True
        except:
            return False

    @staticmethod
    def file_exists_on_remote(remote_file_location):
        file_copied = GCloud.copy_file_from_remote(remote_file_location, './temp.txt')
        if file_copied:
            System.run_command('rm ./temp.txt')
            return True
        return False

    @staticmethod
    def is_authenticated():
        account = System.run_command('gcloud config list account --format value(core.account)')
        if len(account):
            return True
        else:
            return False
    
    @staticmethod
    def is_billing_enabled_for_project(project_id):
        billing_enabled_json = subprocess.check_output(['gcloud', 'beta', 'billing', 'projects', 'describe', project_id, '--format', 'json']).decode('utf-8')
        billing_enabled = json.loads(billing_enabled_json)
        return billing_enabled.get('billingEnabled')

    @staticmethod
    def is_using_our_project_id(project_id):
        active_project_id = subprocess.check_output(['gcloud', 'config', 'list', '--format', 'value(core.project)']).decode('utf-8')
        active_project_id = str(active_project_id).replace('\n', '')
        return active_project_id == project_id

    @staticmethod
    def has_template_instance(instance_template_name):
        instance_templates_json = subprocess.check_output(['gcloud', 'compute', 'instance-templates', 'list', '--format', 'json']).decode('utf-8')
        instance_templates = json.loads(instance_templates_json)
        found_matching_instance_template = False
        for instance_template in instance_templates:
            if instance_template.get('name') == instance_template_name:
                found_matching_instance_template = True
                break
        return found_matching_instance_template

    @staticmethod
    def has_firewall_rule(firewall_rule_name):
        firewall_rules_json = subprocess.check_output(['gcloud', 'compute', 'firewall-rules', 'list', '--format', 'json']).decode('utf-8')
        firewall_rules = json.loads(firewall_rules_json)
        found_matching_firewall_rule = False
        for firewall_rule in firewall_rules:
            if firewall_rule.get('name') == firewall_rule_name:
                found_matching_firewall_rule = True
        return found_matching_firewall_rule

    @staticmethod
    def get_instance(instance_name):
        instances_json = subprocess.check_output(['gcloud', 'compute', 'instances', 'list', '--format', 'json']).decode('utf-8')
        instances = json.loads(instances_json)
        instance = None
        for instance_to_check in instances:
            if instance_to_check.get('name') == instance_name:
                instance = instance_to_check
                break
        return instance

    @staticmethod
    def has_instance(instance_name):
        return GCloud.get_instance(instance_name) != None

    @staticmethod
    def instance_is_running(instance_name):
        instance = GCloud.get_instance(instance_name)
        return instance.get('status') == 'RUNNING'

    @staticmethod
    def get_url(instance_name):
        instance = GCloud.get_instance(instance_name)
        url = instance.get('networkInterfaces')[0].get('accessConfigs')[0].get('natIP')
        return "http://" + url

    @staticmethod
    def update_sdk():
        System.run_command('gcloud components update')

    @staticmethod
    def login():
        System.run_command('gcloud auth login')

    @staticmethod
    def create_project(project_id, project_name):
        System.run_command('gcloud projects create {} --name="{}" --set-as-default'.format(project_id, project_name))
        System.run_command('gcloud config set project {}'.format(project_id))
    
    @staticmethod
    def prompt_for_billing_id(project_id):
        os.system('gcloud alpha billing accounts list')
        billing_account_id = input("Enter billing Account ID from above (if none exist create one here https://cloud.google.com/billing/docs/how-to/manage-billing-account): ")
        System.run_command('gcloud beta billing projects link {} --billing-account={}'.format(project_id, billing_account_id))
    
    @staticmethod
    def upload_file_to_bucket(file_location, bucket_name):
        buckets_list = System.run_command('gsutil ls')
        if bucket_name not in buckets_list:
            System.run_command('gsutil mb gs://{}/'.format(bucket_name))
        System.run_command('gsutil cp {} gs://{}/'.format(file_location, bucket_name))
    
    def upload_directory_to_bucket(directory, bucket_name):
        buckets_list = System.run_command('gsutil ls')
        if bucket_name not in buckets_list:
            System.run_command('gsutil mb gs://{}/'.format(bucket_name))
        System.run_command('gsutil cp -r {} gs://{}/'.format(directory, bucket_name))