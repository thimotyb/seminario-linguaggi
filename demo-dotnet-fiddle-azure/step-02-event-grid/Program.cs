using System;
using Azure.Messaging.EventGrid;

public record DeploymentEvent(
    string Application,
    string Environment,
    string Version,
    bool Successful,
    int DurationSeconds);

public class Program
{
    public static void Main()
    {
        var payload = new DeploymentEvent(
            "billing-api", "production", "2.4.0", Successful: true, 72);

        var cloudEvent = new EventGridEvent(
            subject: "/applications/billing-api",
            eventType: "Seminar.Deployment.Completed",
            dataVersion: "1.0",
            data: payload);

        Console.WriteLine($"Event type : {cloudEvent.EventType}");
        Console.WriteLine($"Subject    : {cloudEvent.Subject}");
        Console.WriteLine($"Event id   : {cloudEvent.Id}");
        Console.WriteLine($"JSON data  : {cloudEvent.Data}");
    }
}

