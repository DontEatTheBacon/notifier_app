import delta

if __name__ == "__main__":
    for section in delta.get_sections():
        print(section.section_number)