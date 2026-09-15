using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
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
        var events = new List<EventGridEvent>
        {
            CreateEvent(new("billing-api", "production", "2.4.0", true, 72)),
            CreateEvent(new("catalog-api", "production", "3.1.0", false, 51)),
            CreateEvent(new("portal", "staging", "8.0.2", true, 130))
        };

        var deployments = events.Select(Handle).ToList();
        var successful = deployments.Count(item => item.Successful);
        var averageDuration = deployments.Average(item => item.DurationSeconds);

        Console.WriteLine();
        Console.WriteLine(
            $"Summary: {successful}/{deployments.Count} successful " +
            $"- average duration {averageDuration:F0}s");
    }

    private static EventGridEvent CreateEvent(DeploymentEvent payload) =>
        new(
            subject: $"/applications/{payload.Application}",
            eventType: "Seminar.Deployment.Completed",
            dataVersion: "1.0",
            data: payload);

    private static DeploymentEvent Handle(EventGridEvent cloudEvent)
    {
        var payload = cloudEvent.Data.ToObjectFromJson<DeploymentEvent>(
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true })!;

        var action = (payload.Environment, payload.Successful, payload.DurationSeconds) switch
        {
            ("production", false, _) => "START ROLLBACK",
            (_, false, _) => "NOTIFY THE TEAM",
            (_, true, > 120) => "CHECK PERFORMANCE",
            _ => "RELEASE COMPLETED"
        };

        var icon = payload.Successful ? "✅" : "❌";
        Console.WriteLine(
            $"{icon} {payload.Application} {payload.Version} " +
            $"[{payload.Environment}] -> {action}");

        return payload;
    }
}

