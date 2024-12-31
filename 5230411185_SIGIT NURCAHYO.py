import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("5230411185_SIGIT NURCAHYO")
        self.root.geometry("800x600")  # Set ukuran jendela

        # Koneksi Database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Ganti dengan password MySQL Anda
            database="retail_db"
        )
        self.cursor = self.db.cursor()

        self.create_database()
        self.create_tables()

        # Tabs
        self.tabs = ttk.Notebook(self.root)
        self.product_tab = ttk.Frame(self.tabs)
        self.transaction_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.product_tab, text="Manajemen Produk")
        self.tabs.add(self.transaction_tab, text="Proses Transaksi")
        self.tabs.pack(expand=1, fill="both")

        # UI Manajemen Produk
        self.setup_product_tab()

        # UI Transaksi
        self.setup_transaction_tab()

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS retail_db;")
        self.cursor.execute("USE retail_db;")

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS produk (
            id_produk INT AUTO_INCREMENT PRIMARY KEY,
            nama_produk VARCHAR(100) NOT NULL,
            harga_produk DECIMAL(65, 10) NOT NULL
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
            id_produk INT NOT NULL,
            jumlah_produk INT NOT NULL,
            total_harga DECIMAL(65, 10) NOT NULL,
            tanggal_transaksi DATE NOT NULL,
            FOREIGN KEY (id_produk) REFERENCES produk(id_produk)
        );
        """)
        self.db.commit()

    def setup_product_tab(self):
        frame_top = ttk.LabelFrame(self.product_tab, text="Form Produk")
        frame_top.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Label dan entri untuk manajemen produk
        ttk.Label(frame_top, text="Nama Produk:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.product_name = ttk.Entry(frame_top)
        self.product_name.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame_top, text="Harga Produk:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.product_price = ttk.Entry(frame_top)
        self.product_price.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(frame_top, text="Tambah Produk", command=self.add_product).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(frame_top, text="Update Produk", command=self.update_product).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(frame_top, text="Hapus Produk", command=self.delete_product).grid(row=2, column=2, padx=10, pady=10)

        # Daftar Produk
        frame_bottom = ttk.LabelFrame(self.product_tab, text="Daftar Produk")
        frame_bottom.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.product_list = ttk.Treeview(frame_bottom, columns=("ID", "Nama", "Harga"), show="headings")
        self.product_list.heading("ID", text="ID")
        self.product_list.heading("Nama", text="Nama Produk")
        self.product_list.heading("Harga", text="Harga Produk")
        self.product_list.column("ID", width=50)
        self.product_list.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Tambahkan scrollbar
        scrollbar = ttk.Scrollbar(frame_bottom, orient="vertical", command=self.product_list.yview)
        self.product_list.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.refresh_product_list()

    def setup_transaction_tab(self):
        frame_top = ttk.LabelFrame(self.transaction_tab, text="Form Transaksi")
        frame_top.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Label dan dropdown untuk transaksi
        ttk.Label(frame_top, text="Pilih Produk:").grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Inisialisasi product_dropdown sebagai atribut objek
        self.product_dropdown = ttk.Combobox(frame_top)
        self.product_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(frame_top, text="Jumlah Produk:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.product_quantity = ttk.Entry(frame_top)
        self.product_quantity.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(frame_top, text="Tambah Transaksi", command=self.add_transaction).grid(row=2, column=0, pady=10)
        ttk.Button(frame_top, text="Hapus Transaksi", command=self.delete_transaction).grid(row=2, column=1, pady=10)

        # Daftar Transaksi
        frame_bottom = ttk.LabelFrame(self.transaction_tab, text="Daftar Transaksi")
        frame_bottom.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.transaction_list = ttk.Treeview(frame_bottom, columns=("ID", "Nama", "Jumlah", "Total", "Tanggal"), show="headings")
        self.transaction_list.heading("ID", text="ID")
        self.transaction_list.heading("Nama", text="Nama Produk")
        self.transaction_list.heading("Jumlah", text="Jumlah")
        self.transaction_list.heading("Total", text="Total Harga")
        self.transaction_list.heading("Tanggal", text="Tanggal")
        self.transaction_list.column("Tanggal", width=200)
        self.transaction_list.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Tambahkan scrollbar
        scrollbar = ttk.Scrollbar(frame_bottom, orient="vertical", command=self.transaction_list.yview)
        self.transaction_list.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.refresh_transaction_list()

    def add_product(self):
        name = self.product_name.get()
        price = self.product_price.get()

        if not name or not price:
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        try:
            price = float(price)
            self.cursor.execute("INSERT INTO produk (nama_produk, harga_produk) VALUES (%s, %s)", (name, price))
            self.db.commit()
            self.refresh_product_list()
            self.product_name.delete(0, tk.END)
            self.product_price.delete(0, tk.END)
            messagebox.showinfo("Sukses", "Produk berhasil ditambahkan.")
        except ValueError:
            messagebox.showerror("Error", "Harga harus berupa angka.")

    def update_product(self):
        selected = self.product_list.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih produk yang ingin diupdate.")
            return

        item = self.product_list.item(selected)
        product_id = item["values"][0]
        name = self.product_name.get()
        price = self.product_price.get()

        if not name or not price:
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        try:
            price = float(price)
            self.cursor.execute("UPDATE produk SET nama_produk=%s, harga_produk=%s WHERE id_produk=%s", (name, price, product_id))
            self.db.commit()
            self.refresh_product_list()
            self.product_name.delete(0, tk.END)
            self.product_price.delete(0, tk.END)
            messagebox.showinfo("Sukses", "Produk berhasil diupdate.")
        except ValueError:
            messagebox.showerror("Error", "Harga harus berupa angka.")

    def delete_product(self):
        selected = self.product_list.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih produk yang ingin dihapus.")
            return

        item = self.product_list.item(selected)
        product_id = item["values"][0]

        # Konfirmasi penghapusan
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus produk ini beserta transaksinya?"):
            try:
                self.cursor.execute("DELETE FROM transaksi WHERE id_produk=%s", (product_id,))
                self.cursor.execute("DELETE FROM produk WHERE id_produk=%s", (product_id,))
                self.db.commit()
                self.refresh_product_list()
                messagebox.showinfo("Sukses", "Produk berhasil dihapus.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Gagal menghapus produk: {e}")

    def refresh_product_list(self):
        for row in self.product_list.get_children():
            self.product_list.delete(row)

        self.cursor.execute("SELECT * FROM produk")
        for row in self.cursor.fetchall():
            # Format harga dengan titik sebagai pemisah ribuan tanpa desimal (misal 10000 menjadi 10.000)
            formatted_row = (row[0], row[1], f"{row[2]:,.0f}".replace(',', '.'))
            self.product_list.insert("", tk.END, values=formatted_row)

        self.refresh_product_dropdown()

    def refresh_product_dropdown(self):
        if not hasattr(self, 'product_dropdown'):
            return  # Hentikan jika dropdown belum diinisialisasi
        
        self.cursor.execute("SELECT id_produk, nama_produk FROM produk")
        products = [f"{row[0]} - {row[1]}" for row in self.cursor.fetchall()]
        self.product_dropdown["values"] = products

    def add_transaction(self):
        selected_product = self.product_dropdown.get()
        quantity = self.product_quantity.get()

        if not selected_product or not quantity:
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        try:
            product_id = int(selected_product.split(" - ")[0])
            quantity = int(quantity)

            if quantity <= 0:
                raise ValueError("Jumlah harus lebih dari 0.")

            self.cursor.execute("SELECT harga_produk FROM produk WHERE id_produk = %s", (product_id,))
            price = self.cursor.fetchone()[0]
            total_price = price * quantity

            self.cursor.execute(
                "INSERT INTO transaksi (id_produk, jumlah_produk, total_harga, tanggal_transaksi) VALUES (%s, %s, %s, %s)",
                (product_id, quantity, total_price, datetime.now())
            )
            self.db.commit()
            self.refresh_transaction_list()
            self.product_quantity.delete(0, tk.END)
            messagebox.showinfo("Sukses", "Transaksi berhasil ditambahkan.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_transaction(self):
        selected = self.transaction_list.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih transaksi yang ingin dihapus.")
            return

        item = self.transaction_list.item(selected)
        transaction_id = item["values"][0]

        # Konfirmasi penghapusan
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus transaksi ini?"):
            try:
                self.cursor.execute("DELETE FROM transaksi WHERE id_transaksi=%s", (transaction_id,))
                self.db.commit()
                self.refresh_transaction_list()
                messagebox.showinfo("Sukses", "Transaksi berhasil dihapus.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Gagal menghapus transaksi: {e}")

    def refresh_transaction_list(self):
        for row in self.transaction_list.get_children():
            self.transaction_list.delete(row)

        self.cursor.execute(
            "SELECT t.id_transaksi, p.nama_produk, t.jumlah_produk, FORMAT(t.total_harga, 0), t.tanggal_transaksi "
            "FROM transaksi t JOIN produk p ON t.id_produk = p.id_produk"
        )
        for row in self.cursor.fetchall():
            self.transaction_list.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()
