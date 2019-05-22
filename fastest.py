import asyncio


class how:

    def __init__(self):
        print("BOOOOM")

    async def snmp(self):
        print("Doing the snmp thing")
        await asyncio.sleep(1)

    async def proxy(self):
        print("Doing the proxy thing")
        await asyncio.sleep(2)

    async def main(self):
        while True:
            await self.snmp()
            await self.proxy()

    def crazt(self):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.main()) # However if you need to create task from arbitrary awaitable, you should use asyncio.ensure_future(obj) vs. loop.create_task(self.main())
        loop.run_forever()


howOb = how()
howOb.crazt()













'''
class how:

    async def test(self):
        print("\nnever scheduled\n\n\n")

    async def main(self):
        await self.test()

    def crazt(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())
        # asyncio.run(self.main())


howOb = how()
howOb.crazt()




import asyncio


class how:

    async def myWorker(self):
        print("Hello World")

    async def main(self):
        print("My Main")

    def crazt(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.gather(*[self.myWorker() for i in range(5)]))
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

howOb = how()
howOb.crazt()




class how:
    def __init__(self):
        print("1_MINI")
    
    
    def called(self):
        print("3_I got called")

    async def test():
        print("\nnever scheduled\n\n\n")

    async def mains():
        await test()
    
    def main(self):
        print("2_lets call a func")
        self.called()

howObject = how()
howObject.main()
asyncio.run(howObject.mains())
'''