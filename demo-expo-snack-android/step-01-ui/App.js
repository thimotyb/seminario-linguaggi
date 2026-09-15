import React from "react";
import { SafeAreaView, StyleSheet, Text, View } from "react-native";

const requirements = [
  "Build automatizzata",
  "Configurazione esterna",
  "Log centralizzati",
];

export default function App() {
  return (
    <SafeAreaView style={styles.screen}>
      <View style={styles.container}>
        <Text style={styles.eyebrow}>SEMINARIO · REACT NATIVE</Text>
        <Text style={styles.title}>Cloud Readiness Check</Text>
        <Text style={styles.subtitle}>
          Una checklist tascabile per discutere i prerequisiti del cloud.
        </Text>

        {requirements.map((requirement) => (
          <View key={requirement} style={styles.card}>
            <Text style={styles.cardIcon}>○</Text>
            <Text style={styles.cardText}>{requirement}</Text>
          </View>
        ))}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#0f172a" },
  container: { flex: 1, padding: 24, paddingTop: 48 },
  eyebrow: { color: "#38bdf8", fontSize: 12, fontWeight: "800", letterSpacing: 1.2 },
  title: { color: "white", fontSize: 34, fontWeight: "800", marginTop: 10 },
  subtitle: { color: "#94a3b8", fontSize: 16, lineHeight: 23, marginTop: 10, marginBottom: 24 },
  card: { flexDirection: "row", alignItems: "center", backgroundColor: "#1e293b", borderRadius: 16, padding: 18, marginBottom: 12 },
  cardIcon: { color: "#38bdf8", fontSize: 24, marginRight: 14 },
  cardText: { color: "#e2e8f0", fontSize: 16, fontWeight: "600" },
});

