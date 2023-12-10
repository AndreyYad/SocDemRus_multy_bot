from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def loop_funcs():
    pass
    
async def set_loop():
    scheduler_repost = AsyncIOScheduler()
    scheduler_repost.add_job(
        loop_funcs, 
        trigger='interval',
        minutes=1
    )
    scheduler_repost.start()