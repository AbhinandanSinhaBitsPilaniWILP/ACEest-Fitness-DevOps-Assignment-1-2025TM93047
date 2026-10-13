import hudson.plugins.git.BranchSpec
import hudson.plugins.git.GitSCM
import hudson.plugins.git.UserRemoteConfig
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import hudson.security.HudsonPrivateSecurityRealm
import jenkins.model.Jenkins
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import org.jenkinsci.plugins.workflow.job.WorkflowJob

def jenkins = Jenkins.get()
def password = System.getenv('JENKINS_EVIDENCE_PASSWORD')
if (!password) {
    throw new IllegalStateException('JENKINS_EVIDENCE_PASSWORD is required')
}

def realm = new HudsonPrivateSecurityRealm(false)
realm.createAccount('evidence-admin', password)
jenkins.setSecurityRealm(realm)
def authorization = new FullControlOnceLoggedInAuthorizationStrategy()
authorization.setAllowAnonymousRead(true)
jenkins.setAuthorizationStrategy(authorization)
jenkins.setNumExecutors(2)
jenkins.save()

def repository = 'https://github.com/AbhinandanSinhaBitsPilaniWILP/ACEest-Fitness-DevOps-Assignment-1-2025TM93047.git'
def remote = new UserRemoteConfig(repository, null, null, null)
def scm = new GitSCM([remote], [new BranchSpec('*/main')], null, null, [])
def job = jenkins.getItem('ACEest-Fitness-DevOps')
if (job == null) {
    job = jenkins.createProject(WorkflowJob, 'ACEest-Fitness-DevOps')
    def definition = new CpsScmFlowDefinition(scm, 'Jenkinsfile')
    definition.setLightweight(true)
    job.setDefinition(definition)
    job.save()
}
job.scheduleBuild2(0)
