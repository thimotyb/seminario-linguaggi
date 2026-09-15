using System;
using System.Collections.Generic;

public record DeploymentEvent(
    string Application,
    string Environment,
    string Version,
    bool Successful,
    int DurationSeconds)
{
    public string Label => $"{Application} {Version} [{Environment}]";
}

public class Program
{
    public static void Main()
    {
        var deployments = new List<DeploymentEvent>
        {
            new("billing-api", "production", "2.4.0", Successful: true, 72),
            new("catalog-api", "production", "3.1.0", Successful: false, 51)
        };

        foreach (var deployment in deployments)
        {
            var action = (deployment.Environment, deployment.Successful) switch
            {
                ("production", false) => "START ROLLBACK",
                (_, false) => "NOTIFY THE TEAM",
                _ => "RELEASE COMPLETED"
            };

            Console.WriteLine($"{deployment.Label} -> {action}");
        }
    }
}

