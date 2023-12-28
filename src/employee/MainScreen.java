package employee;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

public class MainScreen extends JFrame {
    private JTextField nameField, idField, ageField, salaryField;
    private JButton addButton, viewButton;
    private JTextArea employeeListArea;
    private String username, password;

    public MainScreen() {
        // Set up the main frame
        setTitle("Employee Details App");
        setSize(500, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        getUsernameAndPassword();

        // Create components
        nameField = new JTextField(20);
        idField = new JTextField(10);
        ageField = new JTextField(10);
        salaryField = new JTextField(10);
        addButton = new JButton("Add Employee");
        viewButton = new JButton("View Employees");
        employeeListArea = new JTextArea(10, 30);
        employeeListArea.setEditable(false);

        // Set up layout
        setLayout(new BorderLayout());

        // Create panels for different sections
        JPanel inputPanel = new JPanel(new GridLayout(5, 2));
        JPanel buttonPanel = new JPanel(new FlowLayout());
        JScrollPane scrollPane = new JScrollPane(employeeListArea);

        // Add components to inputPanel
        inputPanel.add(new JLabel("Employee ID:"));
        inputPanel.add(idField);
        inputPanel.add(new JLabel("Employee Name:"));
        inputPanel.add(nameField);
   
        inputPanel.add(new JLabel("Age:"));
        inputPanel.add(ageField);
        inputPanel.add(new JLabel("Salary:"));
        inputPanel.add(salaryField);
        inputPanel.add(new JLabel()); // Empty label for spacing
        inputPanel.add(addButton);

        // Add components to buttonPanel
        buttonPanel.add(viewButton);

        // Add panels to the main frame
        add(inputPanel, BorderLayout.NORTH);
        add(buttonPanel, BorderLayout.CENTER);
        add(scrollPane, BorderLayout.SOUTH);

        
        // Add action listeners to the buttons
        addButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Handle the button click event
                addEmployeeToDatabase();
            }
        });

        viewButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Handle the button click event
                displayAllEmployees();
            }
        });
    }

    private void getUsernameAndPassword() {
        while (true) {
            JPanel panel = new JPanel();
            JLabel userLabel = new JLabel("Username:");
            JLabel passLabel = new JLabel("Password:");
            JTextField userField = new JTextField(10);
            JPasswordField passField = new JPasswordField(10);
            panel.add(userLabel);
            panel.add(userField);
            panel.add(passLabel);
            panel.add(passField);

            int result = JOptionPane.showConfirmDialog(null, panel, "Login", JOptionPane.OK_CANCEL_OPTION);
            if (result == JOptionPane.OK_OPTION) {
                String enteredUsername = userField.getText();
                String enteredPassword = new String(passField.getPassword());

                // Check if entered username and password match
                if ("moni".equals(enteredUsername) && "12345".equals(enteredPassword)) {
                   
                    username = enteredUsername;
                    password = enteredPassword;
                    break;
                } else {
        
                    JOptionPane.showMessageDialog(null, "Invalid username or password. Please try again.");
                }
            } else {
                System.exit(0);
            }
        }
    }

    private Connection connect() throws SQLException {
      
        String url = "jdbc:mysql://db4free.net:3306/employee_demo005";
        return DriverManager.getConnection(url, "admin_demo", "12345678@Ap");
    }

    private void addEmployeeToDatabase() {
        // Add employee details to the MySQL database
        try (Connection connection = connect()) {
            String sql = "INSERT INTO employees (empname, empno, age, salary) VALUES (?, ?, ?, ?)";
            try (PreparedStatement statement = connection.prepareStatement(sql)) {
                statement.setString(1, nameField.getText());
                statement.setString(2, idField.getText());
                statement.setInt(3, Integer.parseInt(ageField.getText()));
                statement.setDouble(4, Double.parseDouble(salaryField.getText()));
                statement.executeUpdate();
                JOptionPane.showMessageDialog(null, "Employee added successfully!");
                
                clearFields();
            }
        } catch (SQLException ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(null, "Error adding employee: " + ex.getMessage());
        }
    }

    private void clearFields() {
        nameField.setText("");
        idField.setText("");
        ageField.setText("");
        salaryField.setText("");
    }
    private void displayAllEmployees() {
        // Retrieve and display all employees from the MySQL database
        try (Connection connection = connect()) {
            String sql = "SELECT empname, empno, age, salary FROM employees";
            try (PreparedStatement statement = connection.prepareStatement(sql)) {
                ResultSet resultSet = statement.executeQuery();
                ArrayList<String> employees = new ArrayList<>();
                while (resultSet.next()) {
                    String empname = resultSet.getString("empname");
                    String empno = resultSet.getString("empno");
                    int age = resultSet.getInt("age");
                    double salary = resultSet.getDouble("salary");
                    employees.add("Name: " + empname + ", ID: " + empno + ", Age: " + age + ", Salary: " + salary);
                }
                // Display the list of employees in the JTextArea
                employeeListArea.setText(String.join("\n", employees));
            }
        } catch (SQLException ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(null, "Error retrieving employees: " + ex.getMessage());
        }
    }

    public static void main(String[] args) {
        // Create and display the GUI
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new MainScreen().setVisible(true);
            }
        });
    }
}

