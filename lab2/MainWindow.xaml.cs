using System.Windows;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows.Controls;
using System.Windows.Input;
using Newtonsoft.Json;

namespace lab2
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private DFA dfa;
        public MainWindow()
        {
            InitializeComponent();

            dfa = LoadDFA("dfa_description.json");
        }

        private void CheckButton_Click(object sender, RoutedEventArgs e)
        {
            string inputString = InputTextBox.Text;
            (bool accepted, List<string> configChanges) = dfa.ValidateString(inputString);

            string resultText = string.Join("\n", configChanges);
            if (accepted)
            {
                ResultTextBlock.Text = "Цепочка принадлежит языку";
                MessageBox.Show("Цепочка распознается автоматом!\n\n" + resultText, "Результат");
            }
            else
            {
                ResultTextBlock.Text = "Цепочка не принадлежит языку";
                MessageBox.Show("Цепочка не расознается автоматом!\n\n" + resultText, "Результат");
            }
        }

        private DFA LoadDFA(string filePath)
        {
            string jsonContent = File.ReadAllText(filePath);
            DFAData? data = JsonConvert.DeserializeObject<DFAData>(jsonContent);

            // Создаем словарь переходов
            var transitions = new Dictionary<(string, string), string>();
            foreach (var transition in data.Transitions)
            {
                transitions.Add((transition.From, transition.Input), transition.To);
            }

            // Исправлено: data.AcceptStates вместо data.AcceptState 
            return new DFA(data.States, data.Alphabet, data.StartState, data.AcceptStates, transitions);
        }
    }
    public class DFA
    {
        public List<string> States { get; }
        public List<string> Alphabet { get; }
        public string StartState { get; }
        public string AcceptStates { get; }
        public Dictionary<(string, string), string> Transitions { get; }

        public DFA(List<string> states, List<string> alphabet, string startState, string acceptStates,
            Dictionary<(string, string), string> transitions)
        {
            States = states;
            Alphabet = alphabet;
            StartState = startState;
            AcceptStates = acceptStates;
            Transitions = transitions;
        }

        public (bool, List<string>) ValidateString(string inputString)
        {
            string currentState = StartState;
            List<string> configChanges = new List<string> { $"Начало в состоянии: {currentState}" };
            foreach (char symbol in inputString)
            {
                if (!Alphabet.Contains(symbol.ToString()))
                {
                    return (false, configChanges.Concat(new[] { $"Ошибка: Символ '{symbol}' не принадлежит алфавиту" }).ToList());
                }

                if (!Transitions.ContainsKey((currentState, symbol.ToString())))
                {
                    return (false, configChanges.Concat(new[] { $"Ошибка: Нет перехода для состояния '{currentState}' по символу '{symbol}'" }).ToList());
                }

                string nextState = Transitions[(currentState, symbol.ToString())];
                configChanges.Add($"На символе '{symbol}' переход от {currentState} к {nextState}");
                currentState = nextState;
            }

            if (AcceptStates.Contains(currentState))
            {
                configChanges.Add($"Цепочка завершилась в состоянии: {currentState}");
                return (true, configChanges);
            }
            else
            {
                configChanges.Add($"Цепочка отклонена: завершилась в  состоянии {currentState}");
                return (false, configChanges);
            }
        }
    }

    public class DFAData
    {
        [JsonProperty("states")]
        public List<string>? States { get; set; }
        [JsonProperty("alphabet")]
        public List<string>? Alphabet { get; set; }
        [JsonProperty("start_state")]
        public string? StartState { get; set; }
        [JsonProperty("accept_states")]
        public string? AcceptStates { get; set; }
        public List<Transition>? Transitions { get; set; }
    }

    public class Transition
    {
        [JsonProperty("from")]
        public string? From { get; set; }
        [JsonProperty("input")]
        public string? Input { get; set; }
        [JsonProperty("to")]
        public string? To { get; set; }
    }
}