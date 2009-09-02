#!/usr/bin/python

import Pyro.core
import logging
import task
import task_classes
import sys

class remote_switch( Pyro.core.ObjBase ):
    "class to take remote system control requests" 
    # the task manager can take action on these when convenient.

    def __init__( self, config, tasknames ):
        self.log = logging.getLogger( "main" )
        Pyro.core.ObjBase.__init__(self)
        self.config = config
        self.tasknames = tasknames
        self.task_to_insert = None

        self.set_stop = False
        self.stop_time = None

        self.set_hold = False
        self.hold_time = None

        # record remote system halt requests
        self.system_halt_requested = False

        # record remote system hold requests
        self.system_hold_requested = False
        self.system_resume_requested = False

        # task to abdicate and kill
        self.kill_ids = False
        self.kill_task_ids = {}
        self.kill_rt = False
        self.kill_reftime = None

        # tasks to dump requisites
        self.requisite_dump = False
        self.dump_task_ids = {}

        # task to reset from failed to waiting
        self.reset_a_task = False
        self.reset_task_id = None

        # task to purge
        self.do_purge = False
        self.purge_id = None
        self.purge_stop = None

    def nudge( self ):
        # pretend a task has changed state in order to invoke the event
        # handling loop
        self.log.warning( "REMOTE: nudge requested" )
        task.state_changed = True

    def reset_to_waiting( self, task_id ):
        # reset a failed task to the waiting state
        # (after it has been fixed, presumably!)
        self.log.warning( "REMOTE: reset to waiting: " + task_id )
        self.reset_a_task = True
        self.reset_task_id = task_id

    def insert( self, task_id ):
        # insert a new task into the system
        self.task_to_insert = task_id
        self.log.warning( "REMOTE: task insertion request: " + task_id )

    def hold( self ):
        self.log.warning( "REMOTE: system hold requested" )
        self.system_hold_requested = True

    def get_hold( self ):
        if self.system_hold_requested:
            self.system_hold_requested = False
            return True
        else:
            return False

    def resume( self ):
        self.log.warning( "REMOTE: system resume requested" )
        self.system_resume_requested = True 
        self.system_hold_requested = False 
        # ensure we resume task processing immediately
        task.state_changed = True

    def get_resume( self ):
        if self.system_resume_requested:
            self.system_resume_requested = False
            return True
        else:
            return False

    def set_stop_time( self, reftime ):
        self.log.warning( "REMOTE: set stop time requested" )
        self.set_stop = True
        self.stop_time = reftime

    def set_hold_time( self, reftime ):
        self.log.warning( "REMOTE: set stop time requested" )
        self.set_hold = True
        self.hold_time = reftime

    def shutdown( self ):
        self.log.warning( "REMOTE: system halt requested" )
        self.system_halt_requested = True

    def get_config( self, item ):
        self.log.warning( "REMOTE: config item " + item + " requested" )
        try:
            result = self.config.get( item )
        except:
            self.log.warning( "no such config item: " + item )
        else:
            return result

    def get_task_info( self, task_names ):
        self.log.warning( "REMOTE: task info request for: " + ','.join(task_names ))
        info = {}
        for n in task_names:
            try:
                descr = eval( 'task_classes.' + n + '.describe()' )
            except AttributeError:
                info[ n ] = ['ERROR: No Such Task Class']
            else:
                info[ n ] = descr

        return info

    def dump_task_requisites( self, task_ids ):
        self.log.warning( "REMOTE: requisite dump request for:")
        for task_id in task_ids:
            self.dump_task_ids[ task_id ] = True
            self.log.warning( '-> ' + task_id )
        self.requisite_dump = True

    
    def purge( self, task_id, stop ):
        self.log.warning( "REMOTE: purge request" )
        self.log.warning( '-> ' + task_id + ' and dependees, to ' + stop )

        self.do_purge = True
        self.purge_id = task_id
        self.purge_stop = stop
        task.state_changed = True

    def abdicate_and_kill_rt( self, reftime ):
        self.log.warning( "REMOTE: abdicate and kill request" )
        self.log.warning( '-> all tasks currently in ' + reftime )
        self.kill_rt = True
        self.kill_reftime = reftime
        task.state_changed = True

    def abdicate_and_kill( self, task_ids ):
        self.log.warning( "REMOTE: abdicate and kill request" )
        for task_id in task_ids:
            self.kill_task_ids[ task_id ] = True
            self.log.warning( '-> ' + task_id )
        self.kill_ids = True
        task.state_changed = True

    def set_verbosity( self, level ):
        # change the verbosity of all the logs:
        #   debug, info, warning, error, critical
        self.log.warning( "REMOTE: verbosity change to " + level + " requested"  )
        
        if level == 'debug':
            new_level = logging.DEBUG
        elif level == 'info':
            new_level = logging.INFO
        elif level == 'warning':
            new_level = logging.WARNING
        elif level == 'error':
            new_level = logging.ERROR
        elif level == 'critical':
            new_level = logging.CRITICAL
        else:
            self.log.warning( "no such logging level: " + level )
            return

        self.config.set( 'logging_level', new_level )

        # main log
        self.log.setLevel( new_level )

        # task logs
        # If this run is a restart from state dump file, the following
        # assumes that the configured task list is the same as in the
        # state-dump file, which should be the case.

        for task in self.tasknames:
            # strip off any state string
            foo = task.split(':')
            name = 'main.' + foo[0]
            log = logging.getLogger( name )
            log.setLevel( new_level )
