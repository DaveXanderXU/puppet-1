# application server required cron jobs
class applicationserver::cron {
    cron { 'cleantmpphp':
        ensure  => present,
        command => 'find /tmp -name "php*" -type f -ctime +1 -exec rm -f {} \\;',
        user    => root,
        hour    => 5,
        minute  => 0,
    }
}
