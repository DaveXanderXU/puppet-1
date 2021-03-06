class dumps::copying::labs(
    $labhost = undef,
    $xmldumpsdir = undef,
    $miscdatasetsdir = undef,
) {
    file{ '/usr/local/sbin/labs-rsync-cron.sh':
        ensure  => 'present',
        mode    => '0755',
        content => template('dumps/copying/labs-rsync-cron.sh.erb'),
    }

    cron { 'dumps_labs_rsync':
        ensure      => 'present',
        user        => 'root',
        minute      => '50',
        hour        => '3',
        command     => "/usr/local/sbin/labs-rsync-cron.sh ${xmldumpsdir} ${miscdatasetsdir} ${labhost}",
        environment => 'MAILTO=ops-dumps@wikimedia.org',
        require     => File['/usr/local/sbin/labs-rsync-cron.sh'],
    }
}

