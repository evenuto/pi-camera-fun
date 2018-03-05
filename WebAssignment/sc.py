from crontab import CronTab

my_cron = CronTab(user='pi')
job = my_cron.new(command='python rt.py')
job.minute.every(1)

my_cron.write()

