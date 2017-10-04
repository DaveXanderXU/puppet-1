# == Class releases::proxy_jenkins
#
# A http proxy in front of Jenkins
#
# [*http_port*]
# HTTP port for a Jenkins instance webservice. Example: 8080
#
# [*prefix*]
# The HTTP path used to reach the Jenkins instance. Must have a leading slash.
# Example: /ci
class releases::proxy_jenkins (
    $http_port,
    $prefix,
) {

  # run jenkins behind Apache and have pretty URLs / proxy port 80
  # https://wiki.jenkins-ci.org/display/JENKINS/Running+Jenkins+behind+Apache

  file {
    '/etc/apache2/conf.d/jenkins_proxy':
      ensure => absent,
  }
}