# ruff: noqa: S608  # Possible SQL injection vector through string-based query construction
# Source: https://github.com/fivetran/fivetran_sdk/tree/v2/examples/destination_connector/python
import logging
import sys
import typing as t
from concurrent import futures

import grpc
import sqlalchemy as sa

from cratedb_fivetran_destination.sdk_pb2.common_pb2 import Column
from cratedb_fivetran_destination.util import (
    CrateDBKnowledge,
    Processor,
    TableInfo,
)

from . import read_csv
from .sdk_pb2 import common_pb2, destination_sdk_pb2, destination_sdk_pb2_grpc

INFO = "INFO"
WARNING = "WARNING"
SEVERE = "SEVERE"


logger = logging.getLogger()


class CrateDBDestinationImpl(destination_sdk_pb2_grpc.DestinationConnectorServicer):
    def __init__(self):
        self.metadata = sa.MetaData()
        self.engine: sa.Engine = None
        self.processor: Processor = None

    def ConfigurationForm(self, request, context):
        log_message(INFO, "Fetching configuration form")

        # Create the form fields
        form_fields = common_pb2.ConfigurationFormResponse(
            schema_selection_supported=True, table_selection_supported=True
        )

        # writerType field with dropdown
        writer_type = common_pb2.FormField(
            name="writerType",
            label="Writer Type",
            description="Choose the destination type",
            dropdown_field=common_pb2.DropdownField(dropdown_field=["Database", "File", "Cloud"]),
            default_value="Database",
        )

        # SQLAlchemy database connection URL.
        url = common_pb2.FormField(
            name="url",
            label="SQLAlchemy URL",
            text_field=common_pb2.TextField.PlainText,
            placeholder="crate://localhost:4200",
            default_value="crate://",
        )

        # host field
        host = common_pb2.FormField(
            name="host",
            label="Host",
            text_field=common_pb2.TextField.PlainText,
            placeholder="your_host_details",
        )

        # port field
        port = common_pb2.FormField(
            name="port",
            label="Port",
            text_field=common_pb2.TextField.PlainText,
            placeholder="your_port_details",
        )

        # user field
        user = common_pb2.FormField(
            name="user",
            label="User",
            text_field=common_pb2.TextField.PlainText,
            placeholder="user_name",
        )

        # password field
        password = common_pb2.FormField(
            name="password",
            label="Password",
            text_field=common_pb2.TextField.Password,
            placeholder="your_password",
        )

        # database field
        database = common_pb2.FormField(
            name="database",
            label="Database",
            text_field=common_pb2.TextField.PlainText,
            placeholder="your_database_name",
        )

        # table field
        table = common_pb2.FormField(
            name="table",
            label="Table",
            text_field=common_pb2.TextField.PlainText,
            placeholder="your_table_name",
        )

        # filePath field
        file_path = common_pb2.FormField(
            name="filePath",
            label="File Path",
            text_field=common_pb2.TextField.PlainText,
            placeholder="your_file_path",
        )

        # region field with dropdown
        region = common_pb2.FormField(
            name="region",
            label="Cloud Region",
            description="Choose the cloud region",
            dropdown_field=common_pb2.DropdownField(
                dropdown_field=["Azure", "AWS", "Google Cloud"]
            ),
            default_value="Azure",
        )

        # enableEncryption toggle field
        enable_encryption = common_pb2.FormField(
            name="enableEncryption",
            label="Enable Encryption?",
            description="To enable/disable encryption for data transfer",
            toggle_field=common_pb2.ToggleField(),
        )

        # Define Visibility Conditions for Conditional Fields
        visibility_condition_for_cloud = common_pb2.VisibilityCondition(
            condition_field="writerType", string_value="Cloud"
        )

        visibility_condition_for_database = common_pb2.VisibilityCondition(
            condition_field="writerType", string_value="Database"
        )

        visibility_condition_for_file = common_pb2.VisibilityCondition(
            condition_field="writerType", string_value="File"
        )

        # List of conditional fields
        # Note: The 'name' and 'label' parameters in the
        # FormField for conditional fields are not used.

        # Create conditional fields for Cloud
        conditional_fields_for_cloud = common_pb2.ConditionalFields(
            condition=visibility_condition_for_cloud,
            fields=[host, port, user, password, region],
        )

        # Create conditional fields for File
        conditional_fields_for_file = common_pb2.ConditionalFields(
            condition=visibility_condition_for_file,
            fields=[host, port, user, password, table, file_path],
        )

        # Create conditional fields for Database
        conditional_fields_for_database = common_pb2.ConditionalFields(
            condition=visibility_condition_for_database,
            fields=[url, host, port, user, password, database, table],
        )

        # Add conditional fields to the form
        conditional_field_for_cloud = common_pb2.FormField(
            name="conditional_field_for_cloud",
            label="Conditional field for cloud",
            conditional_fields=conditional_fields_for_cloud,
        )

        conditional_field_for_file = common_pb2.FormField(
            name="conditional_field_for_file",
            label="Conditional field for File",
            conditional_fields=conditional_fields_for_file,
        )

        conditional_field_for_database = common_pb2.FormField(
            name="conditional_field_for_database",
            label="Conditional field for Database",
            conditional_fields=conditional_fields_for_database,
        )

        # Add all fields to the form response
        form_fields.fields.extend(
            [
                writer_type,
                conditional_field_for_file,
                conditional_field_for_cloud,
                conditional_field_for_database,
                enable_encryption,
            ]
        )

        # Add tests to the form
        form_fields.tests.add(name="connect", label="Tests connection")

        form_fields.tests.add(name="select", label="Tests selection")

        return form_fields

    def _configure_database(self, url):
        if not self.engine:
            self.engine = sa.create_engine(url)
            self.processor = Processor(engine=self.engine)

    def Test(self, request, context):
        """
        Verify database connectivity with configured connection parameters.
        """
        log_message(INFO, f"Test database connection: {request.name}")
        self._configure_database(request.configuration.get("url"))
        with self.engine.connect() as connection:
            connection.execute(sa.text("SELECT 42"))
        return common_pb2.TestResponse(success=True)

    def CreateTable(self, request, context):
        """
        Create database table using SQLAlchemy.
        """
        self._configure_database(request.configuration.get("url"))
        logger.info(
            "[CreateTable] :"
            + str(request.schema_name)
            + " | "
            + str(request.table.name)
            + " | "
            + str(request.table.columns)
        )
        table = sa.Table(request.table.name, self.metadata, schema=request.schema_name)
        fivetran_column: Column
        for fivetran_column in request.table.columns:
            db_column: sa.Column = sa.Column()
            db_column.name = CrateDBKnowledge.resolve_field(fivetran_column.name)
            db_column.type = CrateDBKnowledge.resolve_type(fivetran_column.type)
            db_column.primary_key = fivetran_column.primary_key
            if db_column.primary_key:
                db_column.nullable = False
            # TODO: Which kind of parameters are relayed by Fivetran here?
            # db_column.params(fivetran_column.params)  # noqa: ERA001
            table.append_column(db_column)

        # Need to add the `__fivetran_deleted` column manually?
        col: sa.Column = sa.Column(name="__fivetran_deleted")
        col.type = sa.Boolean()
        table.append_column(col)

        table.create(self.engine)
        return destination_sdk_pb2.CreateTableResponse(success=True)

    def AlterTable(self, request, context):
        """
        Alter schema of database table.

        FIXME: Not implemented yet.
        """
        self._configure_database(request.configuration.get("url"))
        res: destination_sdk_pb2.AlterTableResponse  # noqa: F842
        logger.info(
            "[AlterTable]: "
            + str(request.schema_name)
            + " | "
            + str(request.table.name)
            + " | "
            + str(request.table.columns)
        )
        return destination_sdk_pb2.AlterTableResponse(success=True)

    def Truncate(self, request, context):
        """
        Truncate database table.
        """
        self._configure_database(request.configuration.get("url"))
        logger.info(
            "[TruncateTable]: "
            + str(request.schema_name)
            + " | "
            + str(request.table_name)
            + " | soft"
            + str(request.soft)
        )
        with self.engine.connect() as connection:
            connection.execute(
                sa.text(f'DELETE FROM "{request.schema_name}"."{request.table_name}"')
            )
        return destination_sdk_pb2.TruncateResponse(success=True)

    @staticmethod
    def _files_to_records(request, files: t.List[str]):
        """
        Decrypt payload files and generate records.
        """
        for filename in files:
            value = request.keys[filename]
            logger.info(f"Decrypting file: {filename}")
            for record in read_csv.decrypt_file(filename, value):
                # Rename keys according to field map.
                record = CrateDBKnowledge.rename_keys(record)
                yield record

    def WriteBatch(self, request, context):
        """
        Upsert records using SQL.
        """
        self._configure_database(request.configuration.get("url"))

        table = sa.Table(
            request.table.name,
            self.metadata,
            schema=request.schema_name,
            quote_schema=True,
            autoload_with=self.engine,
        )
        primary_keys = [column.name for column in table.primary_key.columns]

        table_info = TableInfo(
            fullname=f'"{request.schema_name}"."{request.table.name}"', primary_keys=primary_keys
        )

        log_message(INFO, f"Data loading started for table: {request.table.name}")
        self.processor.process(
            table_info=table_info,
            upsert_records=self._files_to_records(request, request.replace_files),
            update_records=self._files_to_records(request, request.update_files),
            delete_records=self._files_to_records(request, request.delete_files),
        )
        log_message(INFO, f"Data loading completed for table: {request.table.name}")

        res: destination_sdk_pb2.WriteBatchResponse = destination_sdk_pb2.WriteBatchResponse(
            success=True
        )
        return res

    def DescribeTable(self, request, context):
        """
        Reflect table schema using SQLAlchemy.

        FIXME: Not implemented yet.
        """
        self._configure_database(request.configuration.get("url"))

        column1 = common_pb2.Column(
            name="a1", type=common_pb2.DataType.UNSPECIFIED, primary_key=True
        )
        column2 = common_pb2.Column(name="a2", type=common_pb2.DataType.DOUBLE)
        table: common_pb2.Table = common_pb2.Table(
            name=request.table_name, columns=[column1, column2]
        )
        log_message(SEVERE, "Sample severe message: Completed fetching table info")
        return destination_sdk_pb2.DescribeTableResponse(not_found=False, table=table)


def log_message(level, message):
    print(f'{{"level":"{level}", "message": "{message}", "message-origin": "sdk_destination"}}')  # noqa: T201


def setup_logging(level=logging.INFO, verbose: bool = False):
    if verbose:
        level = logging.DEBUG
    log_format = "%(asctime)-15s [%(name)-26s] %(levelname)-8s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level, force=True)


def start_server():
    setup_logging()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    server.add_insecure_port("[::]:50052")
    destination_sdk_pb2_grpc.add_DestinationConnectorServicer_to_server(
        CrateDBDestinationImpl(), server
    )
    server.start()
    return server


if __name__ == "__main__":  # pragma: no cover
    server = start_server()
    logger.info("Destination gRPC server started")
    server.wait_for_termination()
    logger.info("Destination gRPC server terminated")
