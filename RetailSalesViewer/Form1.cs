using System;
using System.Data;
using System.Data.SqlClient;
using System.Windows.Forms;

namespace RetailSalesViewer
{
    public partial class Form1 : Form
    {
        private readonly string connectionString =
            @"Server=.\SQLEXPRESS;Database=RetailSalesDB;Trusted_Connection=True;";

        public Form1()
        {
            InitializeComponent();
        }

        private void btnIncarca_Click(object sender, EventArgs e)
        {
            IncarcaView();
        }

        private void IncarcaView()
        {
            string query = "SELECT * FROM vw_ValoareComenzi ORDER BY data_comanda";

            try
            {
                using (SqlConnection conn = new SqlConnection(connectionString))
                {
                    using (SqlDataAdapter adapter = new SqlDataAdapter(query, conn))
                    {
                        DataTable dt = new DataTable();
                        adapter.Fill(dt);
                        dataGridView1.DataSource = dt;
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Eroare la încărcarea datelor: " + ex.Message);
            }
        }
    }
}