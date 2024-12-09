using Microsoft.Win32;
using Newtonsoft.Json;
using System.IO;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace lab3
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private DPDA _dpda;
        public MainWindow()
        {
            InitializeComponent();
        }

        private void LoadAutomaton(object sender, RoutedEventArgs e)
        {
            var openFileDialog = new OpenFileDialog
            {
                Filter = "JSON files (*.json)|*.json"
            };

            if (openFileDialog.ShowDialog() == true)
            {
                try
                {
                    _dpda = LoadAutomatonFromFile(openFileDialog.FileName);
                    MessageBox.Show("Автомат загружен успешно!");
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Ошибка загрузки автомата: {ex.Message}");
                }
            }
        }

        private DPDA LoadAutomatonFromFile(string filepath)
        {
            string json;
            using (var reader = new StreamReader(filepath))
            {
                json = reader.ReadToEnd();
            }

            var data = JsonConvert.DeserializeObject<AutomatonData>(json);

            var dpda =  new DPDA(
                data.States,
                data.InputAlphabet,
                data.StackAlphabet,
                data.Transitions,
                data.InitialState,
                data.InitialStackSymbol,
                data.AcceptingStates
            );
            dpda.Reset();
            return dpda;
        }

        private void CheckString(object sender, RoutedEventArgs e)
        {
            if (_dpda == null)
            {
                MessageBox.Show("Сначала загрузите автомат!");
                return;
            }

            HistoryTextBlock.Text = "";

            var inputString = InputTextBox.Text;

            var result = _dpda.Accept(inputString);

            MessageBox.Show(result.Success ? "Цепочка принята" : $"Цепочка отклонена: {result.Reason}");

            HistoryTextBlock.Text = string.Join("\n", _dpda.History);
        }

        public class AutomatonData
        {
            [JsonProperty("states")]
            public List<string> States { get; set; }
            [JsonProperty("input_alphabet")]
            public List<string> InputAlphabet { get; set; }
            [JsonProperty("stack_alphabet")]
            public List<string> StackAlphabet { get; set; }
            [JsonProperty("transitions")]
            public Dictionary<string, List<string>> Transitions { get; set; }
            [JsonProperty("initial_state")]
            public string InitialState { get; set; }
            [JsonProperty("initial_stack_symbol")]
            public string InitialStackSymbol { get; set; }
            [JsonProperty("accepting_states")]
            public List<string> AcceptingStates { get; set; }
        }
    }
}