using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;

namespace FoodCartClass
{
    class Program
    {
        static void Main(string[] args)
        {
            var meanTimeBetweenCustomers = Convert.ToInt32(args[0]);
            var meanServingTime = Convert.ToInt32(args[1]);
            var numberOfWorkers = Convert.ToInt32(args[2]);
            var simulationTime = Convert.ToInt32(args[3]);

            new Simulator().Run(meanTimeBetweenCustomers, meanServingTime, numberOfWorkers, simulationTime);
        }
    }

    public class Simulator
    {
        private int _meanTimeBetweenCustomers;
        private int _meanServingTime;
        private int _numberOfWorkers;
        private int _simulationTime;
        private int _customerNumber = 0;
        private double _totalWaitingTime = 0.0;
        private readonly Stopwatch _stopwatch = Stopwatch.StartNew();

        private readonly Mutex _customerNumberMutex = new Mutex();
        private readonly Mutex _totalWaitingTimeMutex = new Mutex();

        private Semaphore _workers;

        public void Run(in int meanTimeBetweenCustomers, in int meanServingTime, in int numberOfWorkers, in int simulationTime)
        {
            _meanTimeBetweenCustomers = meanTimeBetweenCustomers;
            _meanServingTime = meanServingTime;
            _numberOfWorkers = numberOfWorkers;
            _simulationTime = simulationTime;

            _workers = new Semaphore(_numberOfWorkers, _numberOfWorkers);

            CreateCustomerProcesses();
        }

        private void CreateCustomerProcesses()
        {
            var customers = new List<Thread>();
            do
            {
                Thread.Sleep(_meanTimeBetweenCustomers * 1000);
                var customer = new Thread(CustomerProcess);
                customer.Start();
                customers.Add(customer);
            }
            while (_simulationTime > _stopwatch.ElapsedMilliseconds / 1000.00);


            for (var i = 0; i < customers.Count; ++i)
            {
                customers[i].Join();
            }

            Console.WriteLine($"Number of customers served: {_customerNumber}");
            Console.WriteLine($"Average wait time: {_totalWaitingTime / _customerNumber}");
        }

        private void CustomerProcess(object id)
        {

            var customerStopwatch = Stopwatch.StartNew();

            // Get a customer number
            _customerNumberMutex.WaitOne();
            var customerNumber = ++_customerNumber;
            _customerNumberMutex.ReleaseMutex();

            Console.WriteLine($"At {_stopwatch.ElapsedMilliseconds / 1000} - customer #{customerNumber} walked up.");

            // Wait for a worker to become available
            _workers.WaitOne();
            // Calculate average waiting time
            var waitTime = customerStopwatch.ElapsedMilliseconds / 1000.00;

            // Update the average wait time
            _totalWaitingTimeMutex.WaitOne();
            _totalWaitingTime += waitTime;
            _totalWaitingTimeMutex.ReleaseMutex();

            Console.WriteLine($"At {_stopwatch.ElapsedMilliseconds / 1000} - customer #{customerNumber} is starting to get served.");

            // Customer gets served
            Thread.Sleep(_meanServingTime * 1000);

            Console.WriteLine($"At {_stopwatch.ElapsedMilliseconds / 1000} - customer #{customerNumber} has been served.");

            _workers.Release();

            Console.WriteLine($"At {_stopwatch.ElapsedMilliseconds / 1000} - customer #{customerNumber} has left.");
        }
    }
}
